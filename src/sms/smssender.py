'''
Created on Aug 5, 2014

@author: janaka

This module delivers generated SMS messages to intended users
via IdeaPro SMS API.
'''

from google.appengine.api import urlfetch
from config import settings
import logging
import json

def send(message):
    res = {
        'message': message.content,
        'destinationAddresses': message.phone,
        'password': settings.APP_PASSWORD,
        'applicationId': settings.APP_ID
    }
    
    form_data = json.dumps(res)
    result = urlfetch.fetch(url=settings.SMS_TARGET,
        payload=form_data,
        method=urlfetch.POST,
        headers = {
            'Content-Type': 'application/json',
            'Accept':'application/json'
        }
                            )
    
    if result.status_code == 200:
        logging.info('Message delivered successfully')
    else:
        logging.info('Message delivery failed with error ' + result.status_code)
