'''
@author: janaka

Contains utility functions for application operation
'''

import time
import re


def current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def get_date(time_value):
    return time.strftime('%Y-%m-%d', time_value)


def extract_date(timestamp_str):
    return re.search('\d+-\d+-\d+', timestamp_str).group(0)