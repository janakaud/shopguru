'''
@author: janaka

This module sends an LBS request for a given phone number via IdeaPro LBS API,
blocks till the response is received and returns the response.
'''

from google.appengine.api import urlfetch
from model.entity.location import Location
from config import app_config, util
import logging
import json


def request(phone):
    """ module for sending out LBS requests using the IdeaMart API """
    res = {
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

        # get received time and message content
        received_content = result.content
        decoded_json = json.loads(received_content)

        latitude = decoded_json['latitude']
        longitude = decoded_json['longitude']
        location = Location(latitude, longitude)
        
        logging.info('LBS response: location = (' + latitude + ',' + longitude + ')')
        return location
    else:
        logging.info('LBS request failed with error ' + result.status_code)