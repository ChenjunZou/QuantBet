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
    '平手': 0.0,
    '平手/半球': 0.25,
    '半球': 0.5,
    '半球/一球': 0.75,
    '一球': 1.0,
    '一球/球半': 1.25,
    '球半': 1.5,
    '球半/两球': 1.75,
    '两球': 2.0,
    '两球半/两球半': 2.25,
    '两球半': 2.5,
    '两球半/三球': 2.75,
    '三球': 3.0,
    '受平手/半球': -0.25,
    '受半球': -0.5,
    '受半球/一球': -0.75,
    '受一球': -1.0,
    '受一球/球半': -1.25,
    '受球半': -1.5,
    '受球半/两球': -1.75,
    '受两球': -2.0,
    '受两球半/两球半': -2.25,
    '受两球半': -2.5,
    '受两球半/三球': -2.75,
    '受三球': -3.0,
}
