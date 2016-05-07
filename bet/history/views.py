import logging
from django.shortcuts import render, render_to_response
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.template import RequestContext
import db_utils
from utils.utils import get_param, parse_date_range
import json
from dateutil.relativedelta import relativedelta
from collections import defaultdict

logger = logging.getLogger("bet")
FLOAT_THRESHOLD = 0.01

# Create your views here.
def football(request):
    return football_impl(request)


def sample(request):
    samples = db_utils.get_all_football_games()[1:10]
    params = {'games': samples}
    return render_to_response("history/football.html", params, context_instance=RequestContext(request))


def football_impl(request):
    params = {}
    start_date, end_date = parse_date_range(request)
    league_name = get_param(request, 'league_name', '')
    team = get_param(request, 'team', '')
    params['start_date'] = start_date
    params['end_date'] = end_date
    params['league_name'] = league_name
    params['team'] = team
    games = db_utils.get_all_football_games().filter(datetime__gte=start_date, datetime__lte=end_date)
    if league_name != '':
        games = games.filter(leagueName__contains=league_name)
    if team != '':
        games = games.filter(team__contains=team)
    params['games'] = games
    return render_to_response("history/football.html", params, context_instance=RequestContext(request))


def json_get_football_odds(request, gameID):
    params = {}
    game = db_utils.get_football_game_by_id(gameID)
    # params contain 4 serials : win, lose, draw, and x-axis
    parse_serial(game, params)
    return HttpResponse(json.dumps(params, default=str),  content_type="application/json")


def parse_serial(game, params):
    wins = list()
    draws = list()
    loses = list()
    ous = list()
    handicaps = list()
    win_rows = defaultdict(list)
    draw_rows = defaultdict(list)
    lose_rows = defaultdict(list)
    handicap_rows = defaultdict(list)
    ou_rows = defaultdict(list)

    summaries = db_utils.get_odd_summary(game)
    start_time = db_utils.get_odd_start_time(game)
    end_time = game.datetime
    x_names = get_x_names(start_time, end_time)
    params['x_names'] = x_names
    for summary in summaries:
        details = db_utils.get_odd_details(summary)
        for detail in details:
            time = detail.change_datetime.strftime("%d-%H:%M")
            try:
                x_index = x_names.index(time)
                if detail.cWO >= FLOAT_THRESHOLD:
                    win_rows[summary.vendor].append({'x': x_index, 'y': detail.cWO, 'dt': detail.change_datetime})
                    draw_rows[summary.vendor].append({'x': x_index, 'y': detail.cDO, 'dt': detail.change_datetime})
                    lose_rows[summary.vendor].append({'x': x_index, 'y': detail.cLO, 'dt': detail.change_datetime})
                if detail.cOU >= FLOAT_THRESHOLD:
                    ou_rows[summary.vendor].append({'x': x_index, 'y': float(detail.cOU), 'dt': detail.change_datetime})
                handicap_rows[summary.vendor].append({'x': x_index, 'y': float(detail.cHC), 'dt': detail.change_datetime})
            except ValueError as e:
                logger.exception('time {} is not in x_names, message {}', time, e.message)
                pass

    for row_key in win_rows.iterkeys():
        wins.append({'name': row_key, 'data': win_rows.get(row_key)})
        draws.append({'name': row_key, 'data': draw_rows.get(row_key)})
        loses.append({'name': row_key, 'data': lose_rows.get(row_key)})
        handicaps.append({'name': row_key, 'data': handicap_rows.get(row_key)})
        ous.append({'name': row_key, 'data': ou_rows.get(row_key)})

    params['odd_win'] = wins
    params['odd_draw'] = draws
    params['odd_lose'] = loses
    params['handicap'] = handicaps
    params['over_under'] = ous


def get_x_names(start_time, end_time):
    x_names = []
    delta = relativedelta(minutes=10)
    start_time_minute = start_time.minute / 10 * 10
    start_time = start_time.replace(minute=start_time_minute, second=0, microsecond=0)
    end_time_minute = end_time.minute / 10 * 10
    end_time = end_time.replace(minute=end_time_minute, second=0, microsecond=0)
    current_time = start_time
    while current_time <= end_time:
        x_names.append(current_time.strftime("%d-%H:%M"))
        current_time = current_time + delta
    return x_names

