__author__ = 'tintsing'
from dateutil.relativedelta import relativedelta
from datetime import datetime
from constants import STANDARD_TIME_FORMAT


def remove_nbsp_suffix(raw):
    suffix = '&nbsp;'
    pos = raw.find(suffix)
    if pos != -1:
        return raw[:pos]
    return raw


def date_range(start_dt, end_dt, step=1):
    if step == 1:
        delta = relativedelta(days=1)
    elif step == 2:
        delta = relativedelta(months=1)
    while start_dt <= end_dt:
        yield start_dt
        start_dt = start_dt + delta


def get_season_str(dt):
    month = dt.month
    year = dt.year-2000
    if month < 10:
        return '%02d-%02d' % (year-1, year)
    else:
        return '%02d-%02d' % (year, year+1)


def parse_float(s):
    ret = 0.0
    try:
        ret = float(s)
    except ValueError as e:
        pass
    except TypeError as e:
        pass
    return ret


def parse_int(s):
    ret = 0.0
    try:
        ret = int(s)
    except ValueError as e:
        pass
    except TypeError as e:
        pass
    return ret


def check_if_last_year(first_str, second_str):
    # print first_str, second_str
    first = datetime.strptime(first_str, STANDARD_TIME_FORMAT)
    second = datetime.strptime(second_str, STANDARD_TIME_FORMAT)
    if first < second:
        # double check
        if first.month == 1 and second.month == 12:
            # almost sure
            return True
    return False

