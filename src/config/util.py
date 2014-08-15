'''
@author: janaka

Contains utility functions for application operation
'''

import time
import re


def current_time():
    """ returns current time in MySQL-compatible YYYY-mm-dd HH:MM:SS format """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def get_date(time_value):
    """ returns date from provided timestamp in YYYY-mm-dd format """
    return time.strftime('%Y-%m-%d', time_value)


def extract_date(timestamp_str):
    """ returns date part from timestamp of YYYY-mm-dd HH:MM:SS format """
    return re.search('\d+-\d+-\d+', timestamp_str).group(0)