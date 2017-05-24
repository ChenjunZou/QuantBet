import logging
from django.shortcuts import render, render_to_response
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.template import RequestContext
import db_utils
from utils import get_param, parse_date_range
import json
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from constants import DetailTypes

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

    original_handicap = get_param(request, 'original_handicap', '')
    original_handicap_host = get_param(request, 'original_handicap_host', '')
    original_handicap_away = get_param(request, 'original_handicap_away', '')
    final_handicap = get_param(request, 'final_handicap', '')
    final_handicap_host = get_param(request, 'final_handicap_host', '')
    final_handicap_away = get_param(request, 'final_handicap_away', '')

    params['original_handicap'] = original_handicap
    params['original_handicap_host'] = original_handicap_host
    params['original_handicap_away'] = original_handicap_away

    params['final_handicap'] = final_handicap
    params['final_handicap_host'] = final_handicap_host
    params['final_handicap_away'] = final_handicap_away

    games = db_utils.get_all_football_games().filter(datetime__gte=start_date, datetime__lte=end_date)
    if league_name != '':
        games = games.filter(leagueName__contains=league_name)
    if team != '':
        games = games.filter(team__contains=team)

    if original_handicap != '':
        games = games.filter(footballhistorysummary__iHC=original_handicap)
    if final_handicap != '':
        games = games.filter(footballhistorysummary__fHC=final_handicap)
    params['games'] = games
    return render_to_response("history/football.html", params, context_instance=RequestContext(request))


def basketball(request):
    params = {}
    start_date, end_date = parse_date_range(request)
    league_name = get_param(request, 'league_name', '')
    team = get_param(request, 'team', '')
    params['start_date'] = start_date
    params['end_date'] = end_date
    params['league_name'] = league_name
    params['team'] = team
    games = db_utils.get_all_basketball_games().filter(datetime__gte=start_date, datetime__lte=end_date)
    if league_name != '':
        games = games.filter(league_name__contains=league_name)
    # if team != '':
    #     games = games.filter(team__contains=team)
    params['games'] = games
    return render_to_response("history/basketball.html", params, context_instance=RequestContext(request))


def json_get_football_odds(request, gameID):
    params = {}
    game = db_utils.get_football_game_by_id(gameID)
    # params contain 4 serials : win, lose, draw, and x-axis
    parse_serial(game, params)
    return HttpResponse(json.dumps(params, default=str),  content_type="application/json")


def json_get_basketball_odds(request, gameID):
    params = {}
    details = {}
    game = db_utils.get_basketball_game_by_id(gameID)
    # params['game'] = game
    # params contain 4 serials : win, lose, draw, and x-axis
    for dtype in DetailTypes:
        detail_info = get_basketball_details(gameID, dtype)
        details[dtype.name] = detail_info
    end_time = game.datetime
    start_time = end_time + relativedelta(days=-2)
    x_names = get_x_names(start_time, end_time, interval=1)
    params['x_names'] = x_names
    parse_serial_basketball(game, details, params)
    return HttpResponse(json.dumps(params, default=str),  content_type="application/json")


def get_basketball_details(game_id, detail_type):
    game = db_utils.get_basketball_game_by_id(game_id)
    summaries = db_utils.get_basketball_odd_summary(game)
    for summary in summaries:
        yield (summary.vendor, db_utils.get_basketball_details(summary, detail_type))


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
    end_time = game.datetime
    try:
        start_time = db_utils.get_odd_start_time(game)
    except:
        start_time = end_time + relativedelta(days=-1)
    x_names = get_x_names(start_time, end_time)
    params['x_names'] = x_names
    for summary in summaries:
        details = db_utils.get_odd_details(summary)
        for detail in details:
            time = detail.change_datetime.strftime("%d-%H:%M")
            logger.info(detail)
            try:
                x_index = x_names.index(time)
                if detail.cWO >= FLOAT_THRESHOLD:
                    win_rows[summary.vendor].append({'x': x_index, 'y': detail.cWO, 'dt': detail.change_datetime})
                    draw_rows[summary.vendor].append({'x': x_index, 'y': detail.cDO, 'dt': detail.change_datetime})
                    lose_rows[summary.vendor].append({'x': x_index, 'y': detail.cLO, 'dt': detail.change_datetime})
                if detail.cOU >= FLOAT_THRESHOLD:
                    ou_rows[summary.vendor].append({'x': x_index, 'y': float(detail.cOU), 'dt': detail.change_datetime})
                handicap_rows[summary.vendor].append({'x': x_index, 'y': float(detail.cHCW), 'let': float(detail.cHC), 'dt': detail.change_datetime})
            except ValueError as e:
                logger.exception('time {0} is not in x_names, message {1}'.format(time, e.message))
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


def parse_serial_basketball(game, details, params):
    x_names = params['x_names']
    for dtype in DetailTypes:
        win_rows = defaultdict(list)
        value_rows = defaultdict(list)
        lose_rows = defaultdict(list)
        wins = list()
        values = list()
        loses = list()

        generator = details[dtype.name]
        for detail in generator:
            vendor = detail[0]
            odd_change_details = detail[1]
            for ocd in odd_change_details:
                change_datetime = ocd.datetime.strftime("%d-%H:%M")
                try:
                    x_index = x_names.index(change_datetime)
                    if ocd.value:
                        value_rows[vendor].append({'x': x_index, 'y': float(ocd.value), 'dt': ocd.datetime})
                    else:
                        win_rows[vendor].append({'x': x_index, 'y': float(ocd.win_odd), 'dt': ocd.datetime})
                        lose_rows[vendor].append({'x': x_index, 'y': float(ocd.lose_odd), 'dt': ocd.datetime})
                except ValueError as e:
                    logger.error('time {} is not in x_names, message {}', change_datetime, e.message)
                    pass

        if dtype == DetailTypes.Odd:
            for row_key in win_rows.iterkeys():
                wins.append({'name': row_key, 'data': win_rows.get(row_key)})
                loses.append({'name': row_key, 'data': lose_rows.get(row_key)})
        else:
            for row_key in value_rows.iterkeys():
                values.append({'name': row_key, 'data': value_rows.get(row_key)})
        # print vendor, len(wins), len(loses), len(values)
        params[dtype.name + '_wins'] = wins
        params[dtype.name + '_loses'] = loses
        params[dtype.name + '_values'] = values


def get_x_names(start_time, end_time, interval=10):
    x_names = []
    delta = relativedelta(minutes=interval)
    start_time_minute = start_time.minute / interval * interval
    start_time = start_time.replace(minute=start_time_minute, second=0, microsecond=0)
    end_time_minute = end_time.minute / interval * interval
    end_time = end_time.replace(minute=end_time_minute, second=0, microsecond=0)
    current_time = start_time
    while current_time <= end_time:
        x_names.append(current_time.strftime("%d-%H:%M"))
        current_time = current_time + delta
    return x_names

