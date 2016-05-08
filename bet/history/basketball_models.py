# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from decimal import Decimal


# Create your models here.
class BasketballTeamInfo(models.Model):
    season = models.IntegerField(verbose_name='season number', null=True)
    name = models.CharField(max_length=64)
    datetime = models.DateTimeField()
    round = models.IntegerField(verbose_name='round')
    rank = models.IntegerField()

    def __unicode__(self):
        return u'[%s][%s] %s' % (self.season, self.rank, self.name)


class BasketballGame(models.Model):
    #home_team_info = models.ForeignKey(BasketballTeamInfo, null=True)
    home_name = models.CharField(verbose_name='home team name', max_length=64)
    #away_team_info = models.ForeignKey(BasketballTeamInfo, null=True)
    away_name = models.CharField(verbose_name='away team name', max_length=64)
    league_name = models.CharField(verbose_name='league name', max_length=64)
    TYPE_CHOICE = (('normal', '常规赛'), 'playoff', '季后赛')
    round_type = models.CharField(verbose_name='league type', max_length=16)
    datetime = models.DateTimeField(verbose_name='start time')
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    overtime = models.IntegerField(default=0)

    def __unicode__(self):
        return u'[%s][%s] %s|%s %s:%s' % (self.datetime, self.league_name, self.home_name, self.away_name,
                                          self.home_score, self.away_score)


class BasketballHistorySummary(models.Model):
    game = models.ForeignKey(BasketballGame)
    vendor = models.CharField(verbose_name='basketball bet vendor', max_length=64)
    idt = models.DateTimeField(null=True, blank=True, verbose_name='initial odds datetime')
    iHC = models.DecimalField(null=True, default=Decimal('0.00'), decimal_places=2, max_digits=15,
                              verbose_name='initial handicap')
    iOU = models.DecimalField(null=True, default=Decimal('0.00'), decimal_places=2, max_digits=15,
                              verbose_name='initial over/under')
    iWO = models.FloatField(null=True, verbose_name='initial win odd')
    iDO = models.FloatField(null=True, verbose_name='initial draw odd')
    iLO = models.FloatField(null=True, verbose_name='initial lose odd')
    iHCW = models.FloatField(null=True, verbose_name='initial win odd given handicap')
    iHCL = models.FloatField(null=True, verbose_name='initial lose odd given handicap')
    iOUW = models.FloatField(null=True, verbose_name='initial win odd given over/under')
    iOUL = models.FloatField(null=True, verbose_name='initial lose odd given over/under')

    fHC = models.DecimalField(null=True, default=Decimal('0.00'), decimal_places=2, max_digits=15,
                              verbose_name='final handicap')
    fOU = models.DecimalField(null=True, default=Decimal('0.00'), decimal_places=2, max_digits=15,
                              verbose_name='final over/under')
    fWO = models.FloatField(null=True, verbose_name='final win odd')
    fDO = models.FloatField(null=True, verbose_name='final draw odd')
    fLO = models.FloatField(null=True, verbose_name='final lose odd')
    fHCW = models.FloatField(null=True, verbose_name='final win odd given handicap')
    fHCL = models.FloatField(null=True, verbose_name='final lose odd given handicap')
    fOUW = models.FloatField(null=True, verbose_name='final win odd given over/under')
    fOUL = models.FloatField(null=True, verbose_name='final lose odd given over/under')

    odd_result = models.IntegerField(null=True)
    hc_result = models.IntegerField(null=True)
    ou_result = models.IntegerField(null=True)

    def __unicode__(self):
        return u'%s %s' % (self.game, self.vendor)


class BasketballHistoryDetails(models.Model):
    summary = models.ForeignKey(BasketballHistorySummary)
    datetime = models.DateTimeField(null=True, verbose_name='change odds datetime')
    value = models.DecimalField(null=True, default=Decimal('0.00'), decimal_places=2, max_digits=15)
    win_odd = models.FloatField(null=True, verbose_name='win odd')
    draw_odd = models.FloatField(null=True, verbose_name='draw odd')
    lose_odd = models.FloatField(null=True, verbose_name='lose odd')

    def __unicode__(self):
        return u'%s %s' % (self.summary, self.datetime)


class BasketballHistoryOddDetails(BasketballHistoryDetails):
    pass


class BasketballHistoryHCDetails(BasketballHistoryDetails):
    pass


class BasketballHistoryOUDetails(BasketballHistoryDetails):
    pass


class PlayerInfo(models.Model):
    season = models.IntegerField(verbose_name='season number', null=True)
    name = models.CharField(max_length=64)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()

    def __unicode__(self):
        return u'[%s]%s' % (self.season, self.name)


class BasketballStatistics(models.Model):
    info = models.OneToOneField(PlayerInfo)
    score = models.FloatField()
    rebound = models.FloatField()
    assist = models.FloatField()
    steal = models.FloatField()
    block = models.FloatField
    three_point = models.FloatField()
    turnover = models.FloatField()
    shooting_percent = models.FloatField()
    three_point_percent = models.FloatField()

    def __unicode__(self):
        return u'%s %s %s %s' % (self.info, self.score, self.rebound, self.assist)

