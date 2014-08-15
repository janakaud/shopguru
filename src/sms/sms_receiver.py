'''
@author: janaka
'''

from adapter.webapps import WebappAdapter
from model.entity.message import IncomingSMS
from task import client_handler_factory
from config import util
import logging
import json


class SMSReceiver(WebappAdapter):

    def get(self):
        """ GET request handler -- simply blocks the request """
        # deny access via GET
        logging.info(self.request)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.headers['Accept'] = 'application/json'
        self.response.out.write('Access Denied')

    def post(self):
        """ POST request handler for incoming SMS via IdeaMart API """
        # get received time and message content
        nowTime = util.current_time()
        received_content = self.request.body
        decoded_json = json.loads(received_content)
        requestMessage = decoded_json['message']
        
        # trim off 'tel:' part of sender number
        requestTP = str(decoded_json['sourceAddress'])
        requestTP = requestTP[requestTP.index('tel:')+4:]
        
        message = IncomingSMS(requestTP, nowTime, str(requestMessage))
        
        logging.info('Incoming message: ' + requestMessage + ' from: ' + requestTP)
        
        # delegate messsage processing to client handler
        client_handler_factory.new_client(message).start()