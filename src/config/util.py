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
    return time.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')


def get_difference(timestamp_1, timestamp_2):
    """ returns difference of two timestamps, in hours """
    time_1 = time.strptime(timestamp_1, '%Y-%m-%d %H:%M:%S')
    time_2 = time.strptime(timestamp_2, '%Y-%m-%d %H:%M:%S')
    diff = datetime.fromtimestamp(time_1) - datetime.fromtimestamp(time_2)
    return diff.seconds / 3600  # timedelta has only seconds


def get_delay(timestamp):
    """ returns delay of given timestamp from current time, in hours """
    cur = datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S')
    diff = datetime.fromtimestamp(time.time()) - cur
    return diff.days*24 + diff.seconds/3600


def extract_date(timestamp_str):
    """ returns date part from timestamp of YYYY-mm-dd HH:MM:SS format """
    return re.search('\d+-\d+-\d+', timestamp_str).group(0)