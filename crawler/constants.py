# -*- coding: utf-8 -*-
__author__ = 'tintsing'

# 1.平手(0) 双方平开，双方获胜的几率一样
# 2.平手/半球(0/0.5) 让球方打平买它的人输一半，赢一个全赢
# 3.半球(0.5) 让球方打平或者输球买它的全输，赢一个全赢
# 4.半球/一球(0.5/1) 让球方平或负全输，赢一球赢一半，赢两球全赢
# 5.一球(1) 让球方输、平全输，赢一个球算平，赢两球全赢
# 6.一球/球半(1/1.5) 让球方赢一个球买它的人输一半，赢两球全赢
# 7.球半(1.5) 让球方输、平、赢一个全输，赢两个球全赢
# 8.球半/两球(1.5/2) 让球方赢两个买它的赢一半，赢三个全赢
# 9. 两球(2) 让球方赢两个球算平，赢三个球全赢
HANDICAP_MAP = {
    u'平手': 0.0,
    u'平手/半球': 0.25,
    u'半球': 0.5,
    u'半球/一球': 0.75,
    u'一球': 1.0,
    u'一球/球半': 1.25,
    u'球半': 1.5,
    u'球半/两球': 1.75,
    u'两球': 2.0,
    u'两球/两球半': 2.25,
    u'两球半': 2.5,
    u'两球半/三球': 2.75,
    u'三球': 3.0,
    u'受平手/半球': -0.25,
    u'受半球': -0.5,
    u'受半球/一球': -0.75,
    u'受一球': -1.0,
    u'受一球/球半': -1.25,
    u'受球半': -1.5,
    u'受球半/两球': -1.75,
    u'受两球': -2.0,
    u'受两球半/两球半': -2.25,
    u'受两球半': -2.5,
    u'受两球半/三球': -2.75,
    u'受三球': -3.0,
}

STANDARD_TIME_FORMAT = '%Y-%m-%d %H:%M'