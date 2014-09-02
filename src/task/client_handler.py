'''
@author: janaka
'''

import logging
from threading import Thread
from sms import sms_sender, message_parser
from task import query
from config import util 
from lbs import lbs_handler
from model.entity.customer import Customer
from model.entity.shop import Shop
from model.entity.location import Location
from model.entity.message import IncomingSMS, OutgoingSMS
from exception.exception import *


class ClientHandler(Thread):
    '''
    This class handles incoming client requests as separate threads. 
    '''

    def __init__(self, message):
        """ initialize with message """
        Thread.__init__(self)
        self.message = message
    
    def run(self):
        """ control method for client request handling """
        # first, persist the received message
        logging.info(self.message)
        self.message.persist()
        
        # phone number from message itself
        phone = self.message.phone
        reply = None    # reply message
        
        try:
            # logic goes here!
            self.query = message_parser.parse(self.message)
                
            if self.query.type == query.CUST_REGISTER:
                reply = self.register_cust()
            elif self.query.type == query.SHOP_REGISTER:
                reply = self.register_shop()
             
        except QueryException:  #invalid query
            reply = 'Sorry! We could not understand your query.'

        # send response (error/confirmation)
        reply_sms = OutgoingSMS(phone, util.current_time(), reply)
        sms_sender.send(reply_sms)
        reply_sms.persist()

    def register_cust(self):
        """ customer registration workflow """
        # check for customer in database; create only if absent
        name = self.query.params['name']
        phone = self.query.params['phone']
        address = self.query.params['address']
        
        cust = Customer.retrieve(phone)
        
        reply = None    # reply message
        
        if cust != None:    # respond with error if already registered
            reply = ('Sorry ' + name + '! You have already registered to '
            'ShopGuru as a customer'
            ' on ' + util.extract_date(str(cust.reg_time)))
        else:   # register, and confirm
            location = None
            # try to get customer location
            if address is not None and len(address) > 0:
                location = Location(5.23, 89.77)
            else:
                location = lbs_handler.request(phone)
            
            new_cust = Customer(name=name,
                                phone=phone,
                                reg_time=self.query.params['reg_time'],
                                location=location)
            new_cust.persist()
            reply = 'Welcome to ShopGuru, ' + name + '!'
        
        return reply
    
    def register_shop(self):
        """ shop registration workflow """
        # check for customer in database; create only if absent
        name = self.query.params['name']
        phone = self.query.params['phone']
        address = self.query.params['address']
        
        shop = Shop.retrieve(self.query.params['phone'])
        
        reply = None    # reply message
        
        if shop != None:    # respond with error if already registered
            reply = ('Sorry ' + name + '! You have already registered to '
            'ShopGuru as a shop'
            ' on ' + util.extract_date(str(shop.reg_time)))
        else:   # register, and confirm
            location = None
            # try to get customer location
            if address is not None and len(address) > 0:
                location = Location(5.23, 89.77)
            else:
                location = lbs_handler.request(phone)
            
            new_shop = Shop(name=name,
                            phone=phone,
                            address=self.query.params['address'],
                            category=self.query.params['category'],
                            reg_time=self.query.params['reg_time'],
                            location=location)
            new_shop.persist()
            reply = 'Welcome to ShopGuru, ' + name + '!'
        
        return reply