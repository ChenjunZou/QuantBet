# -*- coding: utf-8 -*-
__author__ = 'tintsing'

import requests
import codecs
from datetime import datetime, date
import argparse
import logging
from bs4 import BeautifulSoup
import json
import CrawlerUtils
from SportsOdds import BasketballOdds
import os
import re
import copy


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
    matches = []
    if response['status'] == 'success':
        try:
            matches = response['result']['match']
        except Exception as e:
            logging.warn('failed to load the date of month %s, reason %s' % (params['date'], e.message))
    return matches


def dump(matches, dt, format):
    """
    example:
    {
        vendoer: "macau",
        leagueName: "NBA",
        roundType: "常规赛",
        leagueType: "1",
        leagueId: "1",
        matchTime: "2016-04-13 08:00",
        awayTeamName: "雷霆",
        matchStatus: "-50",
        awayTeamId: "561",
        hostTeamName: "马刺",
        hostTeamId: "649",
        hostScore: "102",
        awayScore: "98",
        matchResult: "3",
        firstHostOdds: "12110",
        firstAwayOdds: "43800",
        hostOdds: "11060",
        awayOdds: "72235",
        jcLetScore: "-12.5",
        jcTotalScore: "202.5",
        letScoreTape: "90",
        totalScoreTape: "2030",
        awayQuarter1Score: "32",
        awayQuarter2Score: "21",
        hostQuarter1Score: "21",
        hostQuarter2Score: "22",
        betId: "236311"
    }
    we can additionally get match details euro bet company statistics, example
    team details: http://live.aicai.com/lc/xyo_236326.html
    euro odd: http://live.aicai.com/lc/xyo_236326_1_ouzhi.html
    euro let odd: http://live.aicai.com/lc/xyo_236326_rfpl.html
    euro over/under odd: http://live.aicai.com/lc/xyo_236326_dxpl.html

    http://live.aicai.com/lc/xyo/bkeuropodds!getOddsDetail.htm?betId=236326&companyId=30
    """
    odd_history = []
    for match in matches:
        odd = BasketballOdds()
        odd.sports_type = 'basketball'
        odd.vendor = 'unknown'
        odd.league = match['leagueName']
        odd.round_type = match['roundType']
        odd.start_time = match['matchTime']
        odd.away = match['awayTeamName']
        odd.host = match['hostTeamName']
        odd.host_score = int(match['hostScore'])
        odd.away_score = int(match['awayScore'])
        print '%s vs %s' % (odd.host, odd.away)
        # 初盘让分
        odd.origin_let_score = float(match['letScoreTape']) / -10.0
        # 初盘大小分
        odd.origin_ou_score = float(match['totalScoreTape']) / 10.0

        odd.let_score = float(match['jcLetScore'])
        odd.ou_score = float(match['jcTotalScore'])
        odd.odd_result = int(match['matchResult'])

        odd.origin_win_odd = float(match['firstHostOdds']) / 10000.0
        odd.origin_lose_odd = float(match['firstAwayOdds']) / 10000.0
        odd.win_odd = float(match['hostOdds']) / 10000.0
        odd.lose_odd = float(match['awayOdds']) / 10000.0
        odd.bet_id = int(match['betId'])
        odd_history.append(odd)

    detail_history = dump_details(odd_history)
    if format == 'text':
        output_file = codecs.open('basketball/basketball-' + date.strftime(dt, '%Y-%m') + '.txt', 'w', encoding='utf-8')
        for odd in detail_history:
            output_file.write(unicode(odd))
        output_file.close()
    elif format == 'json':
        output_file = codecs.open(
            'basketball-' + date.strftime(dt, '%Y-%m') + '.json', 'w', encoding='utf-8')
        # we could not dump matches, we should dump details as well

        def fdefault(o):
            return o.__dict__

        print 'begin to dump'
        json.dump(detail_history, output_file, ensure_ascii=False, default=fdefault)
        print 'dump success %s' % dt
        output_file.close()


def dump_details(overview_history):
    pattern_odd = re.compile('jq_odd_(\d+)')
    pattern_hc = re.compile('jq_let_score_company_(\d+)')
    pattern_ou = re.compile('jq_let_score_company_(\d+)')
    histories = []
    for game in overview_history:
        print game
        game_id = game.bet_id
        company_info = {}
        url_odd_1 = 'http://live.aicai.com/lc/xyo_%s_1_ouzhi.html' % game_id
        url_odd_2 = 'http://live.aicai.com/lc/xyo_%s_2_ouzhi.html' % game_id
        url_hc = 'http://live.sina.aicai.com/lc/xyo_%s_rfpl.html' % game_id
        url_ou = 'http://live.sina.aicai.com/lc/xyo_%s_dxpl.html' % game_id
        url_odd_json = 'http://live.aicai.com/lc/xyo/bkeuropodds!getOddsDetail.htm'
        url_hc_json = 'http://live.aicai.com/lc/xyo/bkletscore!getOddsDetail.htm'
        url_ou_json = 'http://live.aicai.com/lc/xyo/bkscore!getOddsDetail.htm'
        for url in [url_odd_1, url_odd_2]:
            prepare_json(url, url_odd_json, game, pattern_odd, 0, company_info)
        prepare_json(url_hc, url_hc_json, game, pattern_hc, 1, company_info)
        prepare_json(url_ou, url_ou_json, game, pattern_ou, 2, company_info)
        histories += company_info.values()
    return histories


def prepare_json(url, url_json, game, pattern, kind, company_info):
    """
    kind: 0->odd, 1->hc, 2->ou
    """
    game_id = game.bet_id
    company_response = requests.get(url)
    bs = BeautifulSoup(company_response.text, 'lxml')
    # '#dataList table.dataListTable tr'

    companies = bs.select('table.dataListTable tr')
    companies = [company for company in companies if company.get('id') is not None]
    for company in companies:
        vendor = company.select('.company')[0].get_text().strip()
        company_id_str = company.get('id')
        m = pattern.match(company_id_str)
        company_id = m.group(1)
        if vendor not in company_info:
            game_copy = copy.deepcopy(game)
            game_copy.vendor = vendor
            game_copy.company_id = company_id
            company_info[vendor] = game_copy
        else:
            game_copy = company_info[vendor]
        params = {
            'betId': game_id,
            'companyId': company_id
        }
        history_json = json.loads(requests.get(url_json, params=params).text)
        if kind == 0:
            history_json = history_json['result']['dates']
        else: # 1/2
            history_json = history_json['result']['oddsDetailList']
        for change in history_json:
            change_info = dict()
            change_info['dt'] = change['createTime']
            if kind == 0:
                change_info['w'] = CrawlerUtils.parse_float(change['winOdd']) / 10000.0
                change_info['l'] = CrawlerUtils.parse_float(change['loseOdd']) / 10000.0
            else:
                change_info['w'] = CrawlerUtils.parse_float(change['winOdds']) / 10000.0
                change_info['l'] = CrawlerUtils.parse_float(change['loseOdds']) / 10000.0
                change_info['v'] = CrawlerUtils.parse_float(change['tape']) / 10.0
            if kind == 0:
                game_copy.odd_history.append(change_info)
            elif kind == 1:
                game_copy.hc_history.append(change_info)
            elif kind == 2:
                game_copy.ou_history.append(change_info)

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
    format = args.format
else:
    format = 'json'
if args.path:
    path = args.path
    if not os.path.isdir(path):
        os.mkdir(path)
    os.chdir(path)

for cur_date in CrawlerUtils.date_range(from_date, end_date, step=2):
    matches = page_crawler(cur_date)
    dump(matches, cur_date, format)
