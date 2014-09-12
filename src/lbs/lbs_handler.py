'''
@author: janaka

This module sends an LBS request for a given phone number via IdeaPro LBS API,
blocks till the response is received and returns the response.
'''

import urllib2
from urllib2 import HTTPError, URLError
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
    
    location = None

    try:
        req = urllib2.Request(app_config.LBS_TARGET, form_data, {
                                         'Content-Type': 'application/json',
                                         'Accept':'application/json'
                                     })
        result = urllib2.urlopen(req)
        logging.info('LBS request sent successfully!')

        # get received time and message content
        received_content = result.read()
        decoded_json = json.loads(received_content)

        latitude = str(decoded_json['latitude'])
        longitude = str(decoded_json['longitude'])
        location = Location(latitude, longitude)
        
        # acknowledge result
        logging.info('LBS response: location = (' + 
                     latitude + ',' + longitude + ')')
    except HTTPError as e:
        logging.error('LBS request failed with error ' + str(e.code))
    except URLError as e:
        logging.error('LBS request failed with error ' + e.reason)
    
    return location