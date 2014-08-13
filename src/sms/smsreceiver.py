'''
Created on Aug 5, 2014

@author: janaka
'''

from adapters.webapps import WebappAdapter
from sms.smsmessage import SMSMessage
from task import client_handler_factory
import logging
import json
import time

class SMSReceiver(WebappAdapter):


    def get(self):
        logging.info(self.request)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.headers['Accept'] = 'application/json'
        self.response.out.write('Access Denied')


    def post(self):
        nowTime = time.gmtime()
        received_content = self.request.body
        decoded_json = json.loads(received_content)
        
        requestMessage = decoded_json["message"]
        requestTP = decoded_json["sourceAddress"]
        message = SMSMessage(requestTP, nowTime, requestMessage)
        
        logging.info("Incoming message: " + requestMessage + " from: " + requestTP)
        client_handler_factory.new_client(message).start()
