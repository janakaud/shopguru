'''
Created on Aug 5, 2014

@author: janaka
'''

from adapters.WebappAdapter import WebappAdapter
from entity import Message
from task import ClientHandlerFactory
import logging
import json
from time import gmtime

class SMSReceiver(WebappAdapter):

    def get(self):
        logging.info(self.request)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.headers['Accept'] = 'application/json'
        self.response.out.write('Hello, Telco App Runs on this Space')

    def post(self):
        nowTime = gmtime()
        received_content = self.request.body
        decoded_json = json.loads(received_content)
        
        requestMessage = decoded_json["message"]
        requestTP = decoded_json["sourceAddress"]
        message = Message(sender=requestTP, time=nowTime, content=requestMessage)
        
        logging.info("Incoming message: " + requestMessage + " from: " + requestTP + " ***")
        ClientHandlerFactory.newClient(message).start()