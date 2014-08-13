from threading import Thread
from sms import smssender
from sms.smsmessage import SMSMessage 

'''
Created on Aug 8, 2014

@author: janaka
'''

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
        print(self.message)
        reply = SMSMessage(self.message.phone, self.message.time, 
                           self.message.content)
        smssender.send(reply)