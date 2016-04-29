import datetime
import logging

__author__ = 'tintsing'

logger = logging.getLogger("bet")


def parse_time_range(request, start_default=None, end_default=None):
    start_time = start_default if start_default else datetime.datetime.today() + datetime.timedelta(days=-1)
    end_time = end_default if end_default else datetime.datetime.today()
    try:
        start_time_param = get_param(request, 'start_time', cookie=True)
        if start_time_param != '':
            start_time = datetime.datetime.strptime(start_time_param, '%Y-%m-%d %H:%M')

        end_time_param = get_param(request, 'end_time', cookie=True)
        if end_time_param != '':
            end_time = datetime.datetime.strptime(end_time_param, '%Y-%m-%d %H:%M')
    except ValueError as e:
        logger.warning('datetime parse error {}', e.message)
        pass
    return start_time, end_time


def parse_date_range(request, start_default=None, end_default=None, days_default=7):
    start_time = start_default if start_default else datetime.date.today() + datetime.timedelta(days=-days_default)
    end_time = end_default if end_default else datetime.date.today()
    try:
        start_time_param = get_param(request, 'start_date', '')
        if start_time_param != '':
            start_time = datetime.datetime.strptime(start_time_param, '%Y-%m-%d').date()

        end_time_param = get_param(request, 'end_date', '')
        if end_time_param != '':
            end_time = datetime.datetime.strptime(end_time_param, '%Y-%m-%d').date()
    except ValueError as e:
        logger.warning('date parse error {}', e.message)
        pass

    return start_time, end_time


def get_param(request, param_name, default='', cookie=False, meta=False):
    if param_name in request.GET:
        return request.GET[param_name]
    if param_name in request.POST:
        return request.POST[param_name]
    if cookie:
        return request.COOKIES[param_name]
    if meta:
        return request.META[param_name]
    return default


