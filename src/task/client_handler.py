'''
@author: janaka
'''

from threading import Thread
from sms import sms_sender, message_parser
from task import query
from config import util 
from model.entity.customer import Customer
from model.entity.location import Location
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
        # first, persist the received message
        print(self.message)
        self.message.persist()
        
        # logic goes here!
        self.query = message_parser.parse(self.message)
        
        if self.query.type == query.CUST_REGISTER:
            # check for customer in database; create only if absent
            name = self.query.params['name']
            phone = self.query.params['phone']
            cust = Customer.retrieve(phone)
            
            reply = None    # reply message
            
            if cust != None:    # respond with error if already registered
                reply = ('Sorry ' + name + '! You have already registered to '
                'ShopGuru on ' + util.extract_date(str(cust.reg_time)))
            else:   # register, and confirm
                new_cust = Customer(name,
                                    phone,
                                    self.query.params['reg_time'],
                                    Location(5.23, 89.77))
                new_cust.persist()
                reply = 'Welcome to ShopGuru, ' + name + '!'
            
            reply_sms = OutgoingSMS(phone, util.current_time(), reply)
            sms_sender.send(reply_sms)
            reply_sms.persist()