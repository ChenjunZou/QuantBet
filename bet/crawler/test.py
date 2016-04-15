# -*- coding: utf-8 -*-
__author__ = 'tintsing'

import json
import codecs

a = {'aa': "测试"}

f = open('test.txt', 'w')
json.dump(a, f, ensure_ascii=False)
f.close()