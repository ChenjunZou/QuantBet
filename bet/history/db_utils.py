__author__ = 'tintsing'

import models
import logging
from constants import DetailTypes
logger = logging.getLogger("bet")


# football db operation
def get_all_football_games():
    games = models.FootballGame.objects.all()
    return games


def get_league_names():
    leagues = models.FootballGame.objects.values_list('leaagueName')
    return leagues.distinct()


def get_football_game_by_id(gid):
    game = None
    try:
        game = models.FootballGame.objects.get(id=gid)
    except Exception as e:
        logger.exception('could not get game data, id: {}, error message: {}', gid, e.message)
        pass
    return game


def get_odd_summary(game):
    sums = models.FootballHistorySummary.objects.filter(game=game)
    return sums


def get_odd_details(summary):
    details = models.FootballDetails.objects.filter(summary=summary).order_by('change_datetime')
    return details


def get_init_detail(summary):
    detail = models.FootballDetails.objects.filter(summary=summary)
    first = detail.order_by('change_datetime')
    if first is not None:
        return first[0]
    else:
        raise Exception


def get_odd_start_time(game):
    summary = models.FootballHistorySummary.objects.filter(game=game)
    first = summary.order_by('idt')
    if first is not None:
        return first[0].idt
    else:
        raise Exception


# basketball db operation
def get_all_basketball_games():
    games = models.BasketballGame.objects.all()
    return games


def get_basketball_league_names():
    leagues = models.BasketballGame.objects.values_list('leaague_name')
    return leagues.distinct()


def get_basketball_round_type():
    types = models.BasketballGame.objects.values_list('round_type')
    return types.distinct()


def get_basketball_game_by_id(gid):
    game = None
    try:
        game = models.BasketballGame.objects.get(id=gid)
    except Exception as e:
        logger.exception('could not get game data, id: {}, error message: {}', gid, e.message)
        pass
    return game


def get_basketball_odd_summary(game):
    sums = models.BasketballHistorySummary.objects.filter(game=game)
    return sums


def get_basketball_details(summary, detail_type):
    if detail_type == DetailTypes.Odd:
        details = models.BasketballHistoryOddDetails.objects.filter(summary=summary).order_by('datetime')
    elif detail_type == DetailTypes.Handicap:
        details = models.BasketballHistoryHCDetails.objects.filter(summary=summary).order_by('datetime')
    elif detail_type == DetailTypes.OverUnder:
        details = models.BasketballHistoryOUDetails.objects.filter(summary=summary).order_by('datetime')
    return details


def get_basketball_init_detail(summary, detail_type):
    if detail_type == DetailTypes.Odd:
        details = models.BasketballHistoryOddDetails.objects.filter(summary=summary)
    elif detail_type == DetailTypes.Handicap:
        details = models.BasketballHistoryHCDetails.objects.filter(summary=summary)
    elif detail_type == DetailTypes.OverUnder:
        details = models.BasketballHistoryOUDetails.objects.filter(summary=summary)
    first = details.order_by('datetime')
    if first is not None:
        return first[0]
    else:
        raise Exception

