'''
Created on Aug 8, 2014

@author: janaka
'''

from threading import Thread
from sms import sms_sender
from model.entity.message import IncomingSMS, OutgoingSMS 


class ClientHandler(Thread):
    '''
    This class handles incoming client requests as separate threads. 
    '''

    def __init__(self, message):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.message = message
    
    def run(self):
        # for now, persist the received message
        print(self.message)
        self.message.persist()
        
        # send a reply (echo of received message)
        reply = OutgoingSMS(self.message.phone, self.message.time, 
                           self.message.content)
        sms_sender.send(reply)