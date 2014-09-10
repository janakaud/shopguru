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
from model.entity import shop
from model.entity.shop import Shop
from model.entity.location import Location
from model.entity.message import IncomingSMS, OutgoingSMS
from exception.exception import *
from maps import geocoder


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
            elif self.query.type == query.FIND_SHOP:
                reply = self.find_shop()
            elif self.query.type == query.SHOP_STATUS:
                reply = self.check_shop_status()
            elif self.query.type == query.TRACK_SHOP:
                reply = self.track_shop()
            elif self.query.type == query.UNTRACK_SHOP:
                reply = self.untrack_shop()
            elif self.query.type == query.UPDATE_STATUS:
                reply = self.update_shop_status()
            elif self.query.type == query.CUST_UNREGISTER:
                reply = self.unregister_cust()
            elif self.query.type == query.SHOP_UNREGISTER:
                reply = self.unregister_shop()
             
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
            try:
                new_cust.persist()
                reply = 'Welcome to ShopGuru, ' + name + '!'
            except BaseException as e:
                logging.error(e)
                reply = 'Sorry! An error occurred. Please try again.'
        
        return reply
    
    def register_shop(self):
        """ shop registration workflow """
        # check for customer in database; create only if absent
        name = self.query.params['name']
        phone = self.query.params['phone']
        address = self.query.params['address']
        
        shop = Shop.retrieve(phone)
        
        reply = None    # reply message
        
        if shop != None:    # respond with error if already registered
            reply = ('Sorry ' + name + '! You have already registered to '
            'ShopGuru as a shop'
            ' on ' + util.extract_date(str(shop.reg_time)))
        else:   # register, and confirm
            location = None
            # try to get customer location
            if address is not None and len(address) > 0:
                location = geocoder.geocode(address)
            else:
                location = lbs_handler.request(phone)
            
            new_shop = Shop(name=name,
                            phone=phone,
                            address=self.query.params['address'],
                            category=self.query.params['category'],
                            reg_time=self.query.params['reg_time'],
                            location=location)
            try:
                new_shop.persist()
                reply = 'Welcome to ShopGuru, ' + name + '!'
            except BaseException as e:
                logging.error(e)
                reply = 'Sorry! An error occurred. Please try again.'
        
        return reply

    def update_shop_status(self):
        """ shop status update workflow """
        # check for shop; proceed only if a registered shop
        status = self.query.params['status']
        phone = self.query.params['phone']
        
        shop_o = Shop.retrieve(phone)
        
        reply = None    # reply message
        
        if shop_o == None:    # respond with error if not registered
            reply = ('Sorry! You have not yet registered under '
            'ShopGuru as a shop. Please reply with '
            + message_parser.MSG_REG_SHOP + ' to register.')
        else:   # update status, and confirm
            shop_o.status = status
            shop_o.changes = shop.STATUS_CHANGED
            
            try:
                shop_o.persist()
                reply = 'Your shop status was updated successfully!'
            except BaseException as e:
                logging.error(e)
                reply = 'Sorry! An error occurred. Please try again.'
        
        return reply

    def find_shop(self):
        """ find shop(s) of given category: workflow """
        # check customer; proceed only if a registered customer
        category = self.query.params['category']
        phone = self.query.params['phone']
        
        cust = Customer.retrieve(phone)
        
        reply = None    # reply message
        
        if cust == None:    # respond with error if not registered
            reply = ('Sorry! You have not yet registered under '
            'ShopGuru as a customer. Please reply with '
            + message_parser.MSG_REG_CUST + ' to register.')
        else:
            try:
                # get customer's location
                location = lbs_handler.request(phone)
                
                # retrieve best matching shop results
                matches = Shop.search_by_category(location, category)
                reply = ''
                temp = ''
                
                if matches != None:
                    # create a message of at most 160 characters (1 SMS)
                    for match in matches:
                        temp += (match.name + '\n' + match.address + '\n'
                                  '' + match.status + '\n\n')
                        if len(temp.strip()) <= 160:
                            reply = temp.strip()
                        else:
                            break
                else:
                    reply = ('Sorry, no shops were found for the '
                             '' + category + ' category.')
            except BaseException as e:
                logging.error(e)
                reply = 'Sorry! An error occurred. Please try again.'
        
        return reply