# -*- coding: utf-8 -*-
__author__ = 'tintsing'

from django.core.management.base import BaseCommand, CommandError
import os
import json
from history import models
from datetime import datetime
from django.utils import timezone


class Command(BaseCommand):
    args = ''
    help = 'dump data from file'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--data_path', dest='path', help='the data directory')
        parser.add_argument('-f', '--format', dest='format', help='the data format')

    def handle(self, *args, **options):
        self.stdout.write("args: %r\n" % (args, ))
        self.stdout.write("options: %r\n" % options)

        if not options['path'] or not os.path.isdir(options['path']):
            self.stderr.write("Failed to open data path: ", options['path'])
            return
        path = options['path']
        if options.get('format'):
            input_format = options.get('format')
        else:
            input_format = 'json'

        file_list = os.listdir(path)
        os.chdir(path)
        for filename in file_list:
            f = open(filename)
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
                 "let_condition": "半球 ", "lose_odd": 3.55, "away_rank": "18", "draw_odd": 3.3, "away_score": "1", "let_odd_1": 0.0,
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
                fHC = obj.get('let_condition')
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
                game_summary.save()
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
