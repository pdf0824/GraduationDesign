# coding=utf-8

import time
import datetime


def get_week():
    return datetime.datetime.now().isoweekday()


def get_time():
    return time.strftime('%H:%M:%S', time.localtime(time.time()))


def get_date():
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def get_absence(date1, date2):
    pass
