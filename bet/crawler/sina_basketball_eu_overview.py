# -*- coding: utf-8 -*-
__author__ = 'tintsing'

import requests
import codecs
from datetime import datetime, date
import argparse
import logging
import json
import CrawlerUtils
from SportsOdds import BasketballOdds
import os


def page_crawler(dt):
    logging.info("processing the data of %s" % dt)
    base_url = "http://league.aicai.com/lc/league/bkmatchresult!regularAjax.htm"
    #           "?leagueId=1&season=15-16&date=2015-11"
    params = {
        'leagueId': 1,
        'season': CrawlerUtils.get_season_str(dt),
        'date': date.strftime(dt, '%Y-%m'),
    }
    print params
    response = requests.get(base_url, params=params)
    response = json.loads(response.text)

    try:
        matches = response['result']['match']

    except Exception as e:
        logging.warn('failed to load the date of month %s, reason %s' % (params['date'], e.message))
    return matches


def dump(matches, dt, format):
    if format == 'text':
        output_file = codecs.open('basketball/basketball-' + date.strftime(dt, '%Y-%m') + '.txt', 'w', encoding='utf-8')
        for match in matches:
            odd = BasketballOdds()
            odd.leagueName = match['leagueName']
            odd.round_type = match['roundType']
            odd.start_time = datetime.strptime(match['matchTime'], "%Y-%m-%d %H:%M")
            odd.away = match['awayTeamName']
            odd.host = match['hostTeamName']
            odd.host_score = int(match['hostScore'])
            odd.away_score = int(match['awayScore'])
            odd.origin_let_score = float(match['letScoreTape']) / -10.0
            odd.origin_ou_score = float(match['totalScoreTape']) / 10.0
            odd.let_condition = float(match['jcLetScore'])
            odd.ou_score = float(match['jcTotalScore'])
            odd.odd_result = -1 if int(match['matchResult']) == 0 else 1

            odd.origin_host_odd = float(match['firstHostOdds']) / 10000.0
            odd.origin_away_odd = float(match['firstAwayOdds']) / 10000.0
            odd.win_odd = float(match['hostOdds']) / 10000.0
            odd.lose_odd = float(match['awayOdds']) / 10000.0
            output_file.write(unicode(odd))

        output_file.close()
    elif format == 'json':
        output_file = codecs.open(
            'basketball-' + date.strftime(dt, '%Y-%m') + '.json', 'w', encoding='utf-8')
        json.dump(matches, output_file, ensure_ascii=False)
        output_file.close()


parser = argparse.ArgumentParser()
parser.add_argument('--from_date', help="the date start to crawler, format %Y-%m(2016-04)")
parser.add_argument('--end_date', help="end date to stop to crawler, format %Y-%m(2016-04)")
parser.add_argument('-f', '--format', help='output format')
parser.add_argument('-p', '--path', help='output path')
args = parser.parse_args()
if args.from_date:
    from_date = datetime.strptime(args.from_date, '%Y-%m').date()
else:
    from_date = date.today()
if args.end_date:
    end_date = datetime.strptime(args.end_date, '%Y-%m').date()
else:
    end_date = date.today()
if args.format:
    oformat = args.format
else:
    oformat = 'json'
if args.path:
    path = args.path
    if not os.path.isdir(path):
        os.mkdir(path)
    os.chdir(path)

for cur_date in CrawlerUtils.date_range(from_date, end_date, step=2):
    matches = page_crawler(cur_date)
    dump(matches, cur_date, oformat)
