'''
@author: janaka
'''

import logging
from threading import Thread
from sms import sms_sender, message_parser
from task import query
from config import util, app_config
from lbs import lbs_handler
from model.entity.customer import Customer
from model.entity import shop
from model.entity.shop import Shop
from model.entity.location import Location
from model.entity.subscription import Subscription
from model.entity.message import IncomingSMS, OutgoingSMS
from exception.exception import *
from maps import geocoder

''' message templates used in the module '''
# registration errors 
MSG_MISSING_CUST_DETAILS = ('Sorry! You must provide your name and address'
                            ' as\n\n' + message_parser.MSG_REG_CUST)
MSG_MISSING_SHOP_DETAILS = ('Sorry! You must provide shop name, address '
                            'and category  as\n\n' + 
                            message_parser.MSG_REG_SHOP)
MSG_WRONG_REGISTRATION = ('Sorry! You must use\n\n' + 
                          message_parser.MSG_REG_CUST + '\n\nor\n\n' +
                          message_parser.MSG_REG_SHOP + '\n\nto register')
MSG_BAD_QUERY = 'Sorry! We could not understand your query'

# general error
MSG_ERROR = 'Sorry! An error occurred. Please try again.'

# repeat registration
MSG_CUST_ALREADY_REGISTERED = ('Sorry %s! You have already registered to '
                               'ShopGuru as a customer (%s) on %s')
MSG_SHOP_ALREADY_REGISTERED = ('Sorry %s! You have already registered to '
                               'ShopGuru as a shop (%s) on %s')

# not registered
MSG_CUST_NOT_REGISTERED = ('Sorry! You have not yet registered under '
                           'ShopGuru as a customer. Please reply with\n\n'
                           + message_parser.MSG_REG_CUST
                           + '\nto register.')
MSG_SHOP_NOT_REGISTERED = ('Sorry! You have not yet registered under '
                           'ShopGuru as a shop. Please reply with\n\n'
                           + message_parser.MSG_REG_SHOP
                           + '\nto register.')

# find by category
MSG_FOUND_SHOP_FOR_CATEGORY = '%s\n%s\n%s\n\n'
MSG_NO_SHOPS_FOR_CATEGORY = ('Sorry, no shops were found for the ' 
                             '%s category.')

# subscribe
MSG_FOUND_SHOP_FOR_NAME = '%s\n%s\n\n'
MSG_NO_SHOPS_FOR_NAME = 'Sorry! We could not find a matching shop.'
MSG_FOUND_MANY_SHOPS = 'We found multiple shops%s:\n\n'
MSG_BASED_ON_LOCATION = ' based on your current location'

# success
MSG_WELCOME = 'Welcome to ShopGuru, %s!'
MSG_SHOP_STATUS_UPDATED = 'Your shop status was updated successfully!'
MSG_SUBSCRIBED_TO_SHOP = 'You got subscribed under %s successfully'


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
             
        except MissingCustomerNameException as e:  # REG CUST with no name
            logging.info(e)
            reply = MSG_MISSING_CUST_DETAILS
        except (MissingShopNameException, MissingShopCategoryException) as e:
            # REG SHOP with no name
            logging.info(e)
            reply = MSG_MISSING_SHOP_DETAILS
        except RegistrationException as e:  # REG SHOP with no name
            logging.info(e)
            reply = MSG_WRONG_REGISTRATION
        except QueryException as e:  #invalid query
            logging.info(e)
            reply = MSG_BAD_QUERY 

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
            reply = (MSG_CUST_ALREADY_REGISTERED % 
                     (name, cust.name, util.extract_date(str(cust.reg_time))))
        else:   # register, and confirm
            location = None
            # try to get customer location
            if address is not None and len(address) > 0:
                location = geocoder.geocode(address)
            else:
                location = lbs_handler.request(phone)
            
            new_cust = Customer(name=name,
                                phone=phone,
                                reg_time=self.query.params['reg_time'],
                                location=location)
            try:
                new_cust.persist()
                reply = MSG_WELCOME % name
            except BaseException as e:
                logging.error(e)
                reply = MSG_ERROR
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
            reply = (MSG_SHOP_ALREADY_REGISTERED % 
                     (name, shop.name, util.extract_date(str(shop.reg_time))))
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
                reply = MSG_WELCOME % name
            except BaseException as e:
                logging.error(e)
                reply = MSG_ERROR
        return reply

    def update_shop_status(self):
        """ shop status update workflow """
        # check for shop; proceed only if a registered shop
        status = self.query.params['status']
        phone = self.query.params['phone']
        
        shop_o = Shop.retrieve(phone)
        
        reply = None    # reply message
        
        if shop_o == None:    # respond with error if not registered
            reply = MSG_SHOP_NOT_REGISTERED
        else:   # update status, and confirm
            shop_o.status = status
            shop_o.changes = shop.STATUS_CHANGED
            
            try:
                shop_o.persist()
                reply = MSG_SHOP_STATUS_UPDATED
            except BaseException as e:
                logging.error(e)
                reply = MSG_ERROR
        return reply

    def find_shop(self):
        """ find shop(s) of given category: workflow """
        # check customer; proceed only if a registered customer
        category = self.query.params['category']
        phone = self.query.params['phone']
        
        cust = Customer.retrieve(phone)
        
        reply = None    # reply message
        
        if cust == None:    # respond with error if not registered
            reply = MSG_CUST_NOT_REGISTERED
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
                        temp += (MSG_FOUND_SHOP_FOR_CATEGORY % 
                                 (match.name, match.address, match.status))
                        # include at least one result
                        if (len(temp.strip()) <= app_config.MAX_MSG_LENGTH
                            or reply == ''):
                            reply = temp.strip()
                        else:
                            break
                else:
                    reply = MSG_NO_SHOPS_FOR_CATEGORY % category
            except BaseException as e:
                logging.error(e)
                reply = MSG_ERROR
        return reply

    def track_shop(self):
        """ subscribe customer under given shop: workflow """
        # check customer; proceed only if a registered customer
        shop_name = self.query.params['shop']
        address = self.query.params['address']
        phone = self.query.params['phone']
        
        cust = Customer.retrieve(phone)
        
        reply = None    # reply message
        
        if cust == None:    # respond with error if not registered
            reply = MSG_CUST_NOT_REGISTERED
        else:
            shops = None
            
            # did we use customer's location to find the shop?
            location_estimate = False
            
            # search by address (if available)
            if address != None: 
                shops = Shop.search_by_name(name=shop_name, address=address)
            else:
                location_estimate = True
                location = lbs_handler.request(phone)
                shops = Shop.search_by_name(name=shop_name, location=location)
    
            if shops == None:
                reply = MSG_NO_SHOPS_FOR_NAME
            elif len(shops) != 1:
                # more than 1 shop found
                
                # create a message of at most 160 characters (1 SMS)
                temp = MSG_FOUND_MANY_SHOPS
                if location_estimate:
                    # tell the user we used LBS
                    temp = temp % MSG_BASED_ON_LOCATION
                else:
                    temp = temp % ''
                
                # show as many of found shops as possible
                for match in shops:
                    temp += (MSG_FOUND_SHOP_FOR_NAME % 
                             (match.name, match.address))
                    # include at least one result
                    if (len(temp.strip()) <= app_config.MAX_MSG_LENGTH or 
                        reply == ''):
                        reply = temp.strip()
                    else:
                        break
            else:
                # exactly 1 shop found
                try:
                    new_subs = Subscription(cust_phone=cust.phone,
                                            shop_phone=shops[0].phone,
                                            start_time=
                                            self.query.params['start_time'])
                    new_subs.persist()
                    reply = MSG_SUBSCRIBED_TO_SHOP % shops[0].name
                except BaseException as e:
                    logging.error(e)
                    reply = MSG_ERROR
        return reply