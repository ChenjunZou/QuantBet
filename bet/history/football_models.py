# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from decimal import Decimal


# Create your models here.
class FootballGame(models.Model):
    homeTeam = models.CharField(verbose_name='home team name', max_length=64)
    awayTeam = models.CharField(verbose_name='away team name', max_length=64)
    leagueName = models.CharField(verbose_name='league name', max_length=64)
    datetime = models.DateTimeField(verbose_name='start time')
    homeScore = models.IntegerField(default=0)
    awayScore = models.IntegerField(default=0)

    def __unicode__(self):
        return u'[%s][%s] %s|%s %s:%s' % (self.datetime, self.leagueName, self.homeTeam, self.awayTeam,
                                          self.homeScore, self.awayScore)


class FootballHistorySummary(models.Model):
    game = models.ForeignKey(FootballGame)
    VENDOR_CHOICES = (('macau', '澳盘'),)
    vendor = models.CharField(verbose_name='bet vendor', max_length=64)
    idt = models.DateTimeField(null=True, blank=True, verbose_name='initial odds datetime')
    iHC = models.DecimalField(null=True, default=Decimal('0.00'), decimal_places=2, max_digits=15,
                              verbose_name='initial handicap' )
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

    def __unicode__(self):
        return u'%s %s' % (self.game, self.vendor)


class FootballDetails(models.Model):
    summary = models.ForeignKey(FootballHistorySummary)
    change_datetime = models.DateTimeField(verbose_name='initial odds datetime')
    cHC = models.DecimalField(null=True, default=Decimal('0.00'), decimal_places=2, max_digits=15,
                              verbose_name='initial handicap')
    cOU = models.DecimalField(null=True, default=Decimal('0.00'), decimal_places=2, max_digits=15,
                              verbose_name='initial over/under')
    cWO = models.FloatField(null=True, verbose_name='initial win odd')
    cDO = models.FloatField(null=True, verbose_name='initial draw odd')
    cLO = models.FloatField(null=True, verbose_name='initial lose odd')
    cHCW = models.FloatField(null=True, verbose_name='initial win odd given handicap')
    cHCL = models.FloatField(null=True, verbose_name='initial lose odd given handicap')
    cOUW = models.FloatField(null=True, verbose_name='initial win odd given over/under')
    cOUL = models.FloatField(null=True, verbose_name='initial lose odd given over/under')

    def __unicode__(self):
        return u'%s %s' % (self.summary, self.change_datetime)

