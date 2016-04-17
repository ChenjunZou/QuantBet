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
from CrawlerUtils import remove_nbsp_suffix, parse_float, parse_int, date_range
import os


def page_crawler(dt, output):
    logging.info("processing the data of %s" % dt)
    base_url = "http://odds.sports.sina.com.cn/odds/index.php"
    payload = {'type': 1,
               'year': dt.year,
               'month': dt.month,
               'day': dt.day,
    }
    headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, defalte",
                "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
                "Connection": "keep-alive",
                "Content-Type": "application/json",
    }
    #logging.info(payload)
    print payload
    response = requests.post(base_url, params=payload, headers=headers)

    response.encoding = 'gbk'
    bs = BeautifulSoup(response.text, 'lxml')

    table = bs.select('div .TableShell table > tr')
    table2 = [row for row in table if len(row.select('td')) > 0]

    dt_str = dt.strftime('%Y-%m-%d')
    odds_timeline = bs.select('div .TableShell table > tbody')

    table_zip_odds = zip(table2, odds_timeline)

    team_pattern = '(\[(\d+)\])?(.+)vs(\[(\d+)\])?(.+)'
    pattern = re.compile(team_pattern, flags=re.U)

    odd_history = []
    for row, odds in table_zip_odds:
        rt_elems = row.select('td')
        try:
            football = FootballOdds()
            football.vendor = 'macau'
            football.league = rt_elems[0].get_text()
            football.start_time = dt.strftime('%Y-%m-%d ') + rt_elems[1].get_text()
            team_str = rt_elems[2].select('b')[0].get_text()
            match = pattern.match(team_str)
            if match is not None:
                football.host = match.group(3).strip()
                football.away = match.group(6).strip()
                football.host_rank = parse_int(match.group(2))
                football.away_rank = parse_int(match.group(5))
            else:
                logging.warning(u'could not parse team string %s' % team_str)
                raise ValueError()

            football.let_odd_1 = parse_float(remove_nbsp_suffix(rt_elems[3].get_text()))
            football.let_odd_2 = parse_float(remove_nbsp_suffix(rt_elems[5].get_text()))
            football.let_condition = rt_elems[4].get_text()

            football.win_odd = parse_float(remove_nbsp_suffix(rt_elems[6].get_text()))
            football.draw_odd = parse_float(remove_nbsp_suffix(rt_elems[7].get_text()))
            football.lose_odd = parse_float(remove_nbsp_suffix(rt_elems[8].get_text()))

            football.ou_score = parse_float(remove_nbsp_suffix(rt_elems[13].get_text()))
            football.ou_1 = parse_float(remove_nbsp_suffix(rt_elems[12].get_text()))
            football.ou_2 = parse_float(remove_nbsp_suffix(rt_elems[14].get_text()))
            result = rt_elems[15].get_text().strip()
            if result is not None and result != '':
                result = result.split("-")
                football.host_score = result[0]
                football.away_score = result[1]
        except ValueError as e:
            logging.exception('error: %s data: %s' % (e.message, rt_elems))
            continue
        odd_history.append(football)

        odds_change_list = odds.select('td')
        if odds_change_list is not None and len(odds_change_list) > 0:
            odds_change_first_elem = odds_change_list[0]
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
                odd_change.start_time = football.start_time
                odd_change.change_time = dt.strftime('%Y-') + odd_elems_filter[i * 13].get_text()
                odd_change.let_odd_1 = parse_float(remove_nbsp_suffix(odd_elems_filter[1 + i * 13].get_text()))
                odd_change.let_condition = odd_elems_filter[2 + i * 13].get_text()
                odd_change.let_odd_2 = parse_float(remove_nbsp_suffix(odd_elems_filter[3 + i * 13].get_text()))
                odd_change.win_odd = parse_float(remove_nbsp_suffix(odd_elems_filter[4 + i * 13].get_text()))
                odd_change.draw_odd = parse_float(remove_nbsp_suffix(odd_elems_filter[5 + i * 13].get_text()))
                odd_change.lose_odd = parse_float(remove_nbsp_suffix(odd_elems_filter[6 + i * 13].get_text()))
                odd_change.ou_1 = parse_float(odd_elems_filter[10 + i * 13].get_text)
                odd_change.ou_2 = parse_float(odd_elems_filter[12 + i * 13].get_text)
                odd_change.ou_score = football.ou_score
                odd_history.append(odd_change)

    if output == 'text':
        output_file = codecs.open(dt_str + '.txt', 'w', encoding='UTF-8')
        for item in odd_history:
            output_file.write(unicode(item))
        output_file.close()
    elif output == 'json':
        output_file = codecs.open('football-%s-%s.json' % ('macau', date.strftime(dt, '%Y-%m-%d')),
                                  'w', encoding='utf-8')

        def fdefault(o):
            return o.__dict__

        json.dump(odd_history, output_file, ensure_ascii=False, default=fdefault)
        output_file.close()


parser = argparse.ArgumentParser()
parser.add_argument('--from_date', help="the date start to crawler, format %Y-%m-%d(2016-04-01)")
parser.add_argument('--end_date', help="end date to stop to crawler, format %Y-%m-%d(2016-04-01)")
parser.add_argument('-o', '--output', help='output format')
parser.add_argument('-p', '--path', help='output path')
args = parser.parse_args()
if args.from_date:
    from_date = datetime.strptime(args.from_date, '%Y-%m-%d').date()
else:
    from_date = date.today()
if args.end_date:
    end_date = datetime.strptime(args.end_date, '%Y-%m-%d').date()
else:
    end_date = date.today()
if not os.path.isdir(args.path):
    os.mkdir(args.path, 0o755)
os.chdir(args.path)
if args.output:
    output = args.output
else:
    output = 'json'

for cur_date in date_range(from_date, end_date):
    page_crawler(cur_date, output)

