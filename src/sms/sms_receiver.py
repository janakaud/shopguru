'''
Created on Aug 5, 2014

@author: janaka
'''

from adapter.webapps import WebappAdapter
from model.entity.message import IncomingSMS
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
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        received_content = self.request.body
        decoded_json = json.loads(received_content)
        
        requestMessage = decoded_json['message']
        requestTP = str(decoded_json['sourceAddress'])
        requestTP = requestTP[requestTP.index('tel:')+4:]
        message = IncomingSMS(requestTP, nowTime, str(requestMessage))
        
        logging.info('Incoming message: ' + requestMessage + ' from: ' + requestTP)
        client_handler_factory.new_client(message).start()