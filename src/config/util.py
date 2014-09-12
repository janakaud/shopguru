'''
@author: janaka

Contains utility functions for application operation
'''

import time
from datetime import timedelta, datetime
import re


def current_time():
    """ returns current time in MySQL-compatible YYYY-mm-dd HH:MM:SS format """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def get_timestamp(timestamp_str):
    """ converts provided timestamp in YYYY-mm-dd format, to a time object """
    return time.strptime('%Y-%m-%d %H:%M:%S', timestamp_str)


def get_difference(timestamp_1, timestamp_2):
    """ returns difference of two timestamps, in hours """
    time_1 = time.strptime('%Y-%m-%d %H:%M:%S', timestamp_1)
    time_2 = time.strptime('%Y-%m-%d %H:%M:%S', timestamp_2)
    diff = datetime.fromtimestamp(time_1) - datetime.fromtimestamp(time_2)
    return diff.seconds / 3600  # timedelta has only seconds


def get_delay(timestamp):
    """ returns delay of given timestamp from current time, in hours """
    cur = time.strptime('%Y-%m-%d %H:%M:%S', timestamp)
    diff = datetime.fromtimestamp(time.time()) - datetime.fromtimestamp(cur)
    return diff.seconds / 3600  # timedelta has only seconds


def extract_date(timestamp_str):
    """ returns date part from timestamp of YYYY-mm-dd HH:MM:SS format """
    return re.search('\d+-\d+-\d+', timestamp_str).group(0)