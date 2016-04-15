__author__ = 'tintsing'
from dateutil.relativedelta import relativedelta


def remove_nbsp_suffix(raw):
    nbsp_suffix = '&nbsp;'
    pos = raw.find(nbsp_suffix)
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
    print month, year
    if month < 10:
        return '%s-%s' % (year-1, year)
    else:
        return '%s-%s' % (year, year+1)
