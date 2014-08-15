'''
@author: janaka

This module delivers generated SMS messages to intended users
via IdeaPro SMS API.
'''

from google.appengine.api import urlfetch
from config import sms_config
import logging
import json


def send(message):
    """ module for sending out SMS using the IdeaMart API """
    res = {
        'message': message.content,
        'destinationAddresses': message.phone,
        'password': sms_config.APP_PASSWORD,
        'applicationId': sms_config.APP_ID
    }
    
    # fabricate and send API request
    form_data = json.dumps(res)
    result = urlfetch.fetch(url=sms_config.SMS_TARGET,
        payload=form_data,
        method=urlfetch.POST,
        headers = {
            'Content-Type': 'application/json',
            'Accept':'application/json'
        }
                            )
    
    # acknowledge result
    if result.status_code == 200:
        logging.info('Message delivered successfully')
    else:
        logging.info('Message delivery failed with error ' + result.status_code)
