# -*- coding: utf-8 -*-
__author__ = 'tintsing'

from django.core.management.base import BaseCommand, CommandError
import os
import json
from history import models, db_utils
from datetime import datetime,date
from django.utils import timezone
import re


class Command(BaseCommand):
    args = ''
    help = 'load Sina basketball history data from file'

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
            start_date = '1970-01'
        file_list = os.listdir(path)
        os.chdir(path)

        for filename in file_list:
            f = open(filename)
            filename_date = filename[11:18]
            print filename_date
            if filename_date < start_date:
                self.stdout.write('skip %s because it is earlier than start date %s' % (filename_date, start_date))
                continue
            self.stdout.write('filename: %s\n' % filename)
            json_list = json.load(f, encoding='utf-8')
            for obj in json_list:
                host = obj.get('host')
                away = obj.get('away')
                league = obj.get('league')
                start_time = datetime.strptime(obj.get('start_time'), '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
                vendor = obj.get('vendor')
                host_score = obj.get('host_score')
                away_score = obj.get('away_score')
                round_type = obj.get('round_type')

                game, created = models.BasketballGame.\
                    objects.get_or_create(
                        home_name=host,
                        away_name=away,
                        league_name=league,
                        datetime=start_time,
                        defaults={
                            'home_score': host_score,
                            'away_score': away_score,
                            'round_type': round_type,
                        })
                game.save()
                # print 'is game create: %s' % created
                iHC = obj.get('origin_let_score')
                iOU = obj.get('origin_ou_score')
                iWO = obj.get('origin_win_odd')
                iLO = obj.get('origin_lose_odd')

                fHC = obj.get('let_score')
                fOU = obj.get('ou_score')
                fWO = obj.get('win_odd')
                fLO = obj.get('lose_odd')
                odd_result = obj.get('odd_result')
                hc_result = obj.get('let_result')
                ou_result = obj.get('ou_result')

                game_summary, created = models.BasketballHistorySummary.\
                    objects.get_or_create(
                        game=game,
                        vendor=vendor,
                        defaults={
                            'iHC': iHC,
                            'iOU': iOU,
                            'iWO': iWO,
                            'iLO': iLO,
                            'fHC': fHC,
                            'fOU': fOU,
                            'fWO': fWO,
                            'fLO': fLO,
                            'odd_result': odd_result,
                            'hc_result': hc_result,
                            'ou_result': ou_result,
                        })
                game_summary.save()

                odd_history = obj.get('odd_history')
                hc_history = obj.get('hc_history')
                ou_history = obj.get('ou_history')

                for item in odd_history:
                    dt = datetime.strptime(item.get('dt'), '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
                    odd_change = models.BasketballHistoryOddDetails.objects.create(
                        summary=game_summary,
                        defaults={
                            'datetime': dt,
                            'value': item.get('v'),
                            'win_odd': item.get('w'),
                            'lose_odd': item.get('l'),
                        }
                    )
                    odd_change.save()

                for item in odd_history:
                    dt = datetime.strptime(item.get('dt'), '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
                    odd_change = models.BasketballHistoryHCDetails.objects.create(
                        summary=game_summary,
                        defaults={
                            'datetime': dt,
                            'value': item.get('v'),
                            'win_odd': item.get('w'),
                            'lose_odd': item.get('l'),
                        }
                    )
                    odd_change.save()

                for item in odd_history:
                    dt = datetime.strptime(item.get('dt'), '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
                    odd_change = models.BasketballHistoryOUDetails.objects.create(
                        summary=game_summary,
                        defaults={
                            'datetime': dt,
                            'value': item.get('v'),
                            'win_odd': item.get('w'),
                            'lose_odd': item.get('l'),
                        }
                    )
                    odd_change.save()
