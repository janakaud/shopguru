'''
Created on Aug 5, 2014

@author: janaka
'''

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
import logging
import json

class SMSSender(webapp.RequestHandler):

        url='http://localhost:7000/sms/send' # replace: api.dialog.lk:8080
        destinationAddrs = [requestTP];
        appPasswordCode = "password";
        applicationId = "APP_000001";
        
        replyMessage = 'Hello ' + boy + ' & ' + girl + ' You two got ' + str(randomPercentage) + '% of Love! Cheers!';
        
        res = { 'message': replyMessage,
                "destinationAddresses": destinationAddrs,
                "password": appPasswordCode,
                "applicationId": applicationId
        }

        logging.info(res)
        form_data = json.dumps(res)
        logging.info(form_data)
        result = urlfetch.fetch(url=url,
            payload=form_data,
            method=urlfetch.POST,
            headers={'Content-Type': 'application/json','Accept':'application/json'})

        logging.info(result.content)

        if result.status_code == 200:
            logging.info('*** Message delivered Successfully! ****')
        else:
            logging.info('*** Message was not delivered Successfully!! ERROR-CODE: ' + result.status_code + ' ****')
