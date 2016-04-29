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
    print start_date, end_date
    games = db_utils.get_all_football_games().filter(datetime__gte=start_date, datetime__lte=end_date)
    if league_name != '':
        games = games.filter(league_name__like=league_name)
    if team != '':
        games = games.filter(team__like=team)
    params['games'] = games
    return render_to_response("history/football.html", params, context_instance=RequestContext(request))


def json_get_football_odds(request, gameID):
    params = {}
    game = db_utils.get_football_game_by_id(gameID)
    # params contain 4 serials : win, lose, draw, and x-axis
    parse_serial(game, params)
    return HttpResponse(json.dumps(params),  content_type="application/json")


def parse_serial(game, params):
    wins = list()
    draws = list()
    loses = list()
    win_rows = defaultdict(list)
    draw_rows = defaultdict(list)
    lose_rows = defaultdict(list)
    summaries = db_utils.get_odd_summary(game)
    start_time = db_utils.get_odd_start_time(game)
    end_time = game.datetime
    x_names = get_x_names(start_time, end_time)
    params['x_names'] = x_names
    for summary in summaries:
        win_rows[summary.vendor].append({'x': 0, 'y': summary.iWO})
        draw_rows[summary.vendor].append({'x': 0, 'y': summary.iDO})
        lose_rows[summary.vendor].append({'x': 0, 'y': summary.iLO})
        details = db_utils.get_odd_details(summary)
        for detail in details:
            time = detail.change_datetime.strftime("%d-%H:%M")
            try:
                x_index = x_names.index(time)
                win_rows[summary.vendor].append({'x': x_index, 'y': detail.cWO})
                draw_rows[summary.vendor].append({'x': x_index, 'y': detail.cDO})
                lose_rows[summary.vendor].append({'x': x_index, 'y': detail.cLO})
            except ValueError as e:
                logger.exception('time {} is not in x_names, message {}', time, e.message)
                pass

    for row_key in win_rows.iterkeys():
        wins.append({'name': row_key, 'data': win_rows.get(row_key)})
        draws.append({'name': row_key, 'data': draw_rows.get(row_key)})
        loses.append({'name': row_key, 'data': lose_rows.get(row_key)})

    params['odd_win'] = wins
    params['odd_draw'] = draws
    params['odd_lose'] = loses


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

