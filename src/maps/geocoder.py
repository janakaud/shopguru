'''
@author: janaka

This module sends a Google Geocoding API request for a given address,
blocks till the response is received and returns a Location object.
'''

from google.appengine.api import urlfetch
from config import app_config
import logging
import json
from model.entity.location import Location


def geocode(address):
    """ module for converting addresses to coordinates
        using Google Geocoding API """
    '''    res = {
        'applicationId': app_config.APP_ID,
        'password': app_config.APP_PASSWORD,
        'subscriberId': phone,
        'serviceType': 'IMMEDIATE',
        'responseTime': 'NO_DELAY',
        'freshness': 'HIGH',
        'horizontalAccuracy': '1000'
    }
    
    # fabricate and send API request
    form_data = json.dumps(res)
    result = urlfetch.fetch(url=app_config.LBS_TARGET,
                            payload=form_data,
                            method=urlfetch.POST,
                            headers = {
                                'Content-Type': 'application/json',
                                'Accept':'application/json'
                            }
                            )
    
    # acknowledge result
    if result.status_code == 200:
        logging.info('LBS request sent successfully!')
    else:
        logging.info('LBS request failed with error ' + result.status_code)
    '''    
    # process and return Location object
    return Location(5.23, 89.77)