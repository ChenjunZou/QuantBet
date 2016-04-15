# -*- coding: utf-8 -*-
__author__ = 'tintsing'

import requests
from bs4 import BeautifulSoup
import re
import codecs
from datetime import datetime, date
import argparse
import logging
import json
from FootballOdds import FootballOdds
import CrawlerUtils


def page_crawler(dt, output):
    logging.info("processing the data of %s" % dt)
    base_url = "http://odds.sports.sina.com.cn/odds/index.php"
    payload = {'type': 1,
               'year': dt.year,
               'month': dt.month,
               'day': dt.day,
               }
    #logging.info(payload)
    print payload
    response = requests.post(base_url, data=json.dumps(payload))

    response.encoding = 'gbk'
    bs = BeautifulSoup(response.text, 'lxml')

    table = bs.select('div .TableShell table > tr')
    table2 = [row for row in table if len(row.select('td')) > 0]

    dt_str = dt.strftime('%Y-%m-%d')
    odds_timeline = bs.select('div .TableShell table > tbody')

    table_zip_odds = zip(table2, odds_timeline)

    output_file = dt_str + '.txt'
    fout = codecs.open(output_file, 'w', encoding='UTF-8')

    team_pattern_str = '\[(\d+)\](.+)vs\[(\d+)\](.+)'
    team_pattern = re.compile(team_pattern_str)

    odd_history = []
    for row, odds in table_zip_odds:
        rt_elems = row.select('td')
        try:
            football = FootballOdds()
            football.league = rt_elems[0].get_text()
            football.start_time = dt.strftime('%Y-%m-%d ') + rt_elems[1].get_text()
            team_str = rt_elems[2].select('b')[0].get_text()
            match = team_pattern.match(team_str)

            football.host = match.group(2)
            football.away = match.group(4)
            football.host_rank = match.group(1)
            football.away_rank = match.group(3)

            football.let_odds_1 = float(CrawlerUtils.remove_nbsp_suffix(rt_elems[3].get_text()))
            football.let_odd_2 = float(CrawlerUtils.remove_nbsp_suffix(rt_elems[5].get_text()))
            football.let_condition = rt_elems[4].get_text()

            football.win_odd = float(CrawlerUtils.remove_nbsp_suffix(rt_elems[6].get_text()))
            football.draw_odd = float(CrawlerUtils.remove_nbsp_suffix(rt_elems[7].get_text()))
            football.lose_odd = float(CrawlerUtils.remove_nbsp_suffix(rt_elems[8].get_text()))
            result = rt_elems[15].get_text()
            if result is not None and result != '':
                result = result.split("-")
                football.host_score = result[0]
                football.away_score = result[1]

        except Exception as e:
            logging.warn(e.message)
            continue
        odd_history.append(football)

        odds_change_first_elem = odds.select('td')[0]
        odds_change_size = int(odds_change_first_elem.attrs['rowspan'])

        odd_elems = odds.select('td')
        odd_elems_filter = [elem for elem in odd_elems if 'rowspan' not in elem.attrs]

        for i in xrange(odds_change_size):
            odd_change = FootballOdds()
            odd_change.host = football.host
            odd_change.away = football.away
            odd_change.host_rank = football.host_rank
            odd_change.away_rank = football.away_rank
            odd_change.league = football.league
            odd_change.start_time = dt.strftime('%Y-') + odd_elems_filter[i * 13].get_text()
            odd_change.let_odd_1 = odd_elems_filter[1 + i * 13].get_text()
            odd_change.let_condition = odd_elems_filter[2 + i * 13].get_text()
            odd_change.let_odd_2 = odd_elems_filter[3 + i * 13].get_text()
            odd_change.win_odd = odd_elems_filter[4 + i * 13].get_text()
            odd_change.draw_odd = odd_elems_filter[5 + i * 13].get_text()
            odd_change.lose_odd = odd_elems_filter[6 + i * 13].get_text()
            odd_history.append(odd_change)

        if output == 'text':
            for item in odd_history:
                fout.write(unicode(item))
    fout.close()

parser = argparse.ArgumentParser()
parser.add_argument('--from_date', help="the date start to crawler, format %Y-%m-%d(2016-04-01)")
parser.add_argument('--end_date', help="end date to stop to crawler, format %Y-%m-%d(2016-04-01)")
parser.add_argument('-o', '--output', help='output format')
args = parser.parse_args()
if args.from_date:
    from_date = datetime.strptime(args.from_date, '%Y-%m-%d').date()
else:
    from_date = date.today()
if args.end_date:
    end_date = datetime.strptime(args.end_date, '%Y-%m-%d').date()
else:
    end_date = date.today()

output = 'text'

for cur_date in CrawlerUtils.date_range(from_date, end_date):
    page_crawler(cur_date, output)

