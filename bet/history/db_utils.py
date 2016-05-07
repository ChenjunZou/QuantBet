__author__ = 'tintsing'

import models
import logging

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