__author__ = 'tintsing'
from dateutil.relativedelta import relativedelta


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


def parse_float(str):
    ret = 0.0
    try:
        ret = float(str)
    except ValueError as e:
        pass
    except TypeError as e:
        pass
    return ret


def parse_int(str):
    ret = 0.0
    try:
        ret = int(str)
    except ValueError as e:
        pass
    except TypeError as e:
        pass
    return ret

