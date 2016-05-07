# -*- coding: utf-8 -*-
__author__ = 'tintsing'

from django.core.management.base import BaseCommand, CommandError
import os
import json
from history import models, db_utils
from datetime import datetime, date
from django.utils import timezone
import re


class Command(BaseCommand):
    args = ''
    help = 'load Sina football history data from file'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--data_path', dest='path', help='the data directory')
        parser.add_argument('-s', '--start_date', dest='start_date', help='the start date')

    def handle(self, *args, **options):
        self.stdout.write("args: %r\n" % (args, ))
        self.stdout.write("options: %r\n" % options)

        if not options['path'] or not os.path.isdir(options['path']):
            self.stderr.write("Failed to open data path: ", options['path'])
            return
        path = options['path']
        if options.get('start_date'):
            start_date = options.get('start_date')
        else:
            start_date = '1970-01-01'
        file_list = os.listdir(path)
        os.chdir(path)

        for filename in file_list:
            f = open(filename)
            filenamedate = filename[15:25]
            if filenamedate < start_date:
                self.stdout.write('skip %s because it is earlier than start date %s' % (filenamedate, start_date))
                continue
            self.stdout.write('filename: %s\n' % filename)
            summaries = []
            json_list = json.load(f, encoding='utf-8')
            for obj in json_list:
                host = obj.get('host')
                away = obj.get('away')
                league = obj.get('league')
                start_time = datetime.strptime(obj.get('start_time'), '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
                host_rank = obj.get('host_rank')
                away_rank = obj.get('away_rank')
                vendor = obj.get('vendor')
                host_score = obj.get('host_score')
                away_score = obj.get('away_score')

                '''
                {"league": "西甲", "win_odd": 1.9, "ou_result": 0, "let_odds_1": 1.94, "let_result": 0, "start_time": "2016-04-17 00:15",
                 "ou_score": -1, "host_rank": "10", "odd_result": 0, "ou_1": 0.0, "host": "拉斯彭马斯", "host_score": "1",
                 "let_score": 0.5, "lose_odd": 3.55, "away_rank": "18", "draw_odd": 3.3, "away_score": "1", "let_odd_1": 0.0,
                  "away": "希杭", "ou_2": 0.0, "let_odd_2": 1.92}
                '''
                game, created = models.FootballGame.\
                    objects.get_or_create(homeTeam=host, awayTeam=away, leagueName=league, datetime=start_time,
                                defaults={
                                    'homeScore': host_score,
                                    'awayScore': away_score,
                                })
                game.save()
                # print 'is game create: %s' % created
                fHC = obj.get('let_score')
                fOU = obj.get('ou_score')
                fWO = obj.get('win_odd')
                fDO = obj.get('draw_odd')
                fLO = obj.get('lose_odd')
                fHCW = obj.get('let_odd_1')
                fHCL = obj.get('let_odd_2')
                fOUW = obj.get('ou_1')
                fOUL = obj.get('ou_2')
                # print obj
                # print fHC, fOU, fWO, fDO, fLO, fHCW, fHCL, fOUW, fOUL
                game_summary, created = models.FootballHistorySummary.\
                    objects.get_or_create(game=game, vendor=vendor,
                               defaults={
                                   'fHC': fHC,
                                   'fOU': fOU,
                                   'fWO': fWO,
                                   'fDO': fDO,
                                   'fLO': fLO,
                                   'fHCW': fHCW,
                                   'fHCL': fHCL,
                                   'fOUW': fOUW,
                                   'fOUL': fOUL,
                               })
                # print 'is summary created %s' % created
                if not created:
                    ctime = obj.get('change_time')
                    if ctime != '':
                        ctime = datetime.strptime(obj.get('change_time'), '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
                        game_details = models.FootballDetails.\
                            objects.create(summary=game_summary,
                                           change_datetime=ctime,
                                           cHC=fHC,
                                           cOU=fOU,
                                           cWO=fWO,
                                           cDO=fDO,
                                           cLO=fLO,
                                           cHCW=fHCW,
                                           cHCL=fHCL,
                                           cOUW=fOUW,
                                           cOUL=fOUL,
                                       )
                        game_details.save()
                else:
                    game_summary.save()
                    summaries.append(game_summary)
            for summary in summaries:
                try:
                    detail = db_utils.get_init_detail(summary)
                    summary.idt = detail.change_datetime
                    summary.iHC = detail.cHC
                    summary.iOU = detail.cOU
                    summary.iWO = detail.cWO
                    summary.iDO = detail.cDO
                    summary.iLO = detail.cLO
                    summary.iHCW = detail.cHCW
                    summary.iHCL = detail.cHCL
                    summary.iOUW = detail.cOUW
                    summary.iOUL = detail.cOUL
                    summary.save()
                except Exception:
                    print('no detail found for summary %s' % summary)

