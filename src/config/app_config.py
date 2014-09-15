'''
@author: janaka
'''

""" IdeaPro API configurations """
SMS_SOURCE = '/receive'
SMS_TARGET = 'http://127.0.0.1:7000/sms/send' # replace: api.dialog.lk:8080
APP_PASSWORD = 'password'
APP_ID = 'APP_000001'
LBS_TARGET = 'http://127.0.0.1:7000/lbs/locate'
GEOCODE_TARGET = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s'
    # replace %s with URL encoded address
MAX_MSG_LENGTH = 160    # default for SMS