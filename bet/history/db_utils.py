__author__ = 'tintsing'

import models


def get_all_football_game():
    games = models.FootballGame.objects.all()
    return games