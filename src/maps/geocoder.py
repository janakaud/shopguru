'''
@author: janaka

This module sends a Google Geocoding API request for a given address,
blocks till the response is received and returns a Location object.
'''

import urllib2
from urllib2 import HTTPError, URLError
from config import app_config
import logging
import json
import string
from model.entity.location import Location


def geocode(address):
    """ module for converting addresses to coordinates
        using Google Geocoding API """
    
    location = None
    
    # fabricate and send API request (fill address parameter)
    url = app_config.GEOCODE_TARGET % string.replace(address, ' ', '+')
    
    try:
        logging.info('Sending Geocoding API request %s' % url)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)

        # get received time and message content
        received_content = response.read()
        decoded_json = json.loads(received_content)

        # location is located at this position in JSON response
        result = decoded_json['results'][0]['geometry']['location']
        latitude = '%.06f' % float(result['lat'])
        longitude = '%.06f' % float(result['lng'])
        location = Location(latitude, longitude)
        
        # acknowledge result
        logging.info('LBS response: location = (' + 
                     latitude + ',' + longitude + ')')
    except KeyError as e:
        logging.error('Geocoding API returned bad response; ' + str(e))
    except HTTPError as e:
        logging.error('Geocoding API request failed with error ' + str(e.code))
    except BaseException as e:
        logging.error(e)

    # process and return Location object
    return location