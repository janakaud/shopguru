'''
@author: janaka

This module delivers generated SMS messages to intended users
via IdeaPro SMS API.
'''

import urllib2
from urllib2 import HTTPError, URLError
from config import app_config
import logging
import json


def send(message):
    """ module for sending out SMS using the IdeaMart API """
    
    # message length check
    if len(message.content) > app_config.MAX_MSG_LENGTH:
        logging.warn('Message too long, may get truncated')
    
    res = {
        'message': message.content,
        'destinationAddresses': message.phone,
        'password': app_config.APP_PASSWORD,
        'applicationId': app_config.APP_ID
    }
    
    # fabricate and send API request
    form_data = json.dumps(res)
    
    try:
        req = urllib2.Request(app_config.SMS_TARGET, form_data, {
                                         'Content-Type': 'application/json',
                                         'Accept':'application/json'
                                     })
        urllib2.urlopen(req)
        logging.info('Message delivered successfully')
    except HTTPError as e:
        logging.error('Message delivery failed with error ' + str(e.code))
    except URLError as e:
        logging.error('Message delivery failed with error ' + e.reason)