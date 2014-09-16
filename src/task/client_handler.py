'''
@author: janaka
'''

import logging
from threading import Thread
from sms import sms_sender, message_parser
from sms.message_parser import *
from task import query
from config import util, app_config
from lbs import lbs_handler
from model.entity.customer import Customer
from model.entity import shop
from model.entity.shop import Shop
from model.entity.location import Location
from model.entity import subscription
from model.entity.subscription import Subscription
from model.entity.message import IncomingSMS, OutgoingSMS
from exception.exception import *
from maps import geocoder

''' message templates used in the module '''
# registration errors 
MSG_MISSING_CUST_DETAILS = ('Sorry! You must provide your name and address'
                            ' as\n\n' + MSG_REG_CUST)
MSG_MISSING_SHOP_DETAILS = ('Sorry! You must provide shop name, address '
                            'and category  as\n\n' + 
                            MSG_REG_SHOP)
MSG_WRONG_REGISTRATION = ('Sorry! You must use\n\n' + 
                          MSG_REG_CUST + '\n\nor\n\n' +
                          MSG_REG_SHOP + '\n\nto register.')
MSG_WRONG_UNREGISTRATION = ('Sorry! You must use\n\n' + 
                          MSG_UNREG_CUST + '\n\nor\n\n' +
                          MSG_UNREG_SHOP + '\n\nto unregister.')
MSG_BAD_QUERY = 'Sorry! We could not understand your query.'

# input validation errors
MSG_TOO_SHORT = 'Sorry! Please use a longer %s (at least %s letters).'
MSG_TOO_LONG = 'Sorry! Please use a shorter %s (less than %s letters).'

MSG_NAME_TOO_SHORT = MSG_TOO_SHORT % ('name', '%s')
MSG_NAME_TOO_LONG = MSG_TOO_LONG % ('name', '%s')
MSG_ACTUAL_NAME_TOO_SHORT = (MSG_NAME_TOO_SHORT 
                             % str(MIN_NAME_ACTUAL))
MSG_ACTUAL_NAME_TOO_LONG = (MSG_NAME_TOO_LONG
                             % str(MAX_NAME_ACTUAL))
MSG_QUERY_NAME_TOO_SHORT = (MSG_NAME_TOO_SHORT 
                             % str(MIN_NAME_QUERY))
MSG_QUERY_NAME_TOO_LONG = (MSG_NAME_TOO_LONG
                             % str(MAX_NAME_QUERY))

MSG_ADDRESS_TOO_SHORT = MSG_TOO_SHORT % ('address', '%s')
MSG_ADDRESS_TOO_LONG = MSG_TOO_LONG % ('address', '%s')
MSG_ACTUAL_ADDRESS_TOO_SHORT = (MSG_ADDRESS_TOO_SHORT 
                             % str(MIN_ADDRESS_ACTUAL))
MSG_ACTUAL_ADDRESS_TOO_LONG = (MSG_ADDRESS_TOO_LONG
                             % str(MAX_ADDRESS_ACTUAL))
MSG_QUERY_ADDRESS_TOO_SHORT = (MSG_ADDRESS_TOO_SHORT 
                             % str(MIN_ADDRESS_QUERY))
MSG_QUERY_ADDRESS_TOO_LONG = (MSG_ADDRESS_TOO_LONG
                             % str(MAX_ADDRESS_QUERY))

MSG_CATEGORY_TOO_SHORT = MSG_TOO_SHORT % ('category', '%s')
MSG_CATEGORY_TOO_LONG = MSG_TOO_LONG % ('category', '%s')
MSG_ACTUAL_CATEGORY_TOO_SHORT = (MSG_CATEGORY_TOO_SHORT 
                             % str(MIN_CATEGORY_ACTUAL))
MSG_ACTUAL_CATEGORY_TOO_LONG = (MSG_CATEGORY_TOO_LONG
                             % str(MAX_CATEGORY_ACTUAL))
MSG_QUERY_CATEGORY_TOO_SHORT = (MSG_CATEGORY_TOO_SHORT 
                             % str(MIN_CATEGORY_QUERY))
MSG_QUERY_CATEGORY_TOO_LONG = (MSG_CATEGORY_TOO_LONG
                             % str(MAX_CATEGORY_QUERY))

MSG_STATUS_TOO_SHORT = (MSG_TOO_SHORT 
                        % ('status', str(MIN_STATUS)))
MSG_STATUS_TOO_LONG = MSG_TOO_LONG % ('status', str(MAX_STATUS))

# general error
MSG_ERROR = 'Sorry! An error occurred. Please try again.'

# repeat registration
MSG_CUST_ALREADY_REGISTERED = ('Sorry %s! You have already registered to '
                               'ShopGuru as a customer (%s) on %s.')
MSG_SHOP_ALREADY_REGISTERED = ('Sorry %s! You have already registered to '
                               'ShopGuru as a shop (%s) on %s.')

# not registered
MSG_CUST_NOT_REGISTERED = ('Sorry! You have not yet registered under '
                           'ShopGuru as a customer. Please reply with\n\n'
                           + MSG_REG_CUST
                           + '\n\nto register.')
MSG_SHOP_NOT_REGISTERED = ('Sorry! You have not yet registered under '
                           'ShopGuru as a shop. Please reply with\n\n'
                           + MSG_REG_SHOP
                           + '\n\nto register.')

# find by category
MSG_FOUND_SHOP_FOR_CATEGORY = '%s\n%s\n%s\n\n'
MSG_NO_SHOPS_FOR_CATEGORY = ('Sorry %s! no shops were found for the ' 
                             '%s category.')

# subscribe
MSG_FOUND_SHOP_FOR_NAME = '%s\n%s\n\n'
MSG_NO_SHOPS_FOR_NAME = 'Sorry %s! We could not find a matching shop.'
MSG_FOUND_MANY_SHOPS = 'We found multiple shops%s:\n\n'
MSG_BASED_ON_LOCATION = ' based on your current location'

# repeat subscription
MSG_ALREADY_SUBSCRIBED = ('Sorry %s! You have already subscribed under '
                           'the shop %s.')

# unsubscribe errors
MSG_CUST_NOT_SUBSCRIBED = ('Sorry %s! We could not find any subscriptions '
                           'for you.')
MSG_CUST_NOT_SUBSCRIBED_FOR_SHOP = ('Sorry %s! You are not subscribed'
                                    ' under the shop %s.')

# success
MSG_WELCOME = 'Welcome to ShopGuru, %s!'
MSG_SHOP_STATUS_UPDATED = ('%s, your shop status was updated successfully to'
                           ' "%s".')
MSG_SUBSCRIBED_TO_SHOP = '%s, you got subscribed under %s successfully!'
MSG_UNSUBSCRIBED_FROM_SHOP = '%s, you got unsubscribed from %s successfully.'
MSG_GOODBYE = 'Goodbye %s! We hope to see you back at ShopGuru some day!'


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
                
        # missing query registration parameters             
        except MissingCustomerNameException as e:
            logging.info(e)
            reply = MSG_MISSING_CUST_DETAILS
        except (MissingShopNameException, MissingShopCategoryException) as e:
            logging.info(e)
            reply = MSG_MISSING_SHOP_DETAILS
        # input validation errors
        except QueryNameTooShortException as e:
            logging.info(e)
            reply = MSG_QUERY_NAME_TOO_SHORT
        except QueryNameTooLongException as e:
            logging.info(e)
            reply = MSG_QUERY_NAME_TOO_LONG
        except QueryAddressTooShortException as e:
            logging.info(e)
            reply = MSG_QUERY_ADDRESS_TOO_SHORT
        except QueryAddressTooLongException as e:
            logging.info(e)
            reply = MSG_QUERY_ADDRESS_TOO_LONG
        except QueryCategoryTooShortException as e:
            logging.info(e)
            reply = MSG_QUERY_CATEGORY_TOO_SHORT
        except QueryCategoryTooLongException as e:
            logging.info(e)
            reply = MSG_QUERY_CATEGORY_TOO_LONG
        except ActualNameTooShortException as e:
            logging.info(e)
            reply = MSG_ACTUAL_NAME_TOO_SHORT
        except ActualNameTooLongException as e:
            logging.info(e)
            reply = MSG_ACTUAL_NAME_TOO_LONG
        except ActualAddressTooShortException as e:
            logging.info(e)
            reply = MSG_ACTUAL_ADDRESS_TOO_SHORT
        except ActualAddressTooLongException as e:
            logging.info(e)
            reply = MSG_ACTUAL_ADDRESS_TOO_LONG
        except ActualCategoryTooShortException as e:
            logging.info(e)
            reply = MSG_ACTUAL_CATEGORY_TOO_SHORT
        except ActualCategoryTooLongException as e:
            logging.info(e)
            reply = MSG_ACTUAL_CATEGORY_TOO_LONG
        except StatusTooShortException as e:
            logging.info(e)
            reply = MSG_STATUS_TOO_SHORT
        except StatusTooLongException as e:
            logging.info(e)
            reply = MSG_STATUS_TOO_LONG
        except RegistrationException as e:  # REG SHOP with no name
            logging.info(e)
            reply = MSG_WRONG_REGISTRATION
        except UnregistrationException as e:  # REG SHOP with no name
            logging.info(e)
            reply = MSG_WRONG_UNREGISTRATION
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
            logging.info('ERROR: Customer already registered')
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
                logging.info('DONE: Customer registered')
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
            logging.info('ERROR: Shop already registered')
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
                logging.info('DONE: Shop registered')
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
            logging.info('ERROR: Shop not registered')
            reply = MSG_SHOP_NOT_REGISTERED
        else:   # update status, and confirm
            shop_o.status = status
            shop_o.last_update = self.query.params['update_time']
            shop_o.changes = shop.STATUS_CHANGED
            
            try:
                shop_o.persist()
                logging.info('DONE: Shop status updated')
                reply = MSG_SHOP_STATUS_UPDATED % (shop_o.name, status)
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
            logging.info('ERROR: Customer not registered')
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
                    # check if we have any subscribed shops, in list
                    # get all subscriptions of customer
                    subs = Subscription.search_by_cust(cust.phone)
                    if subs != None:
                        # get intersection of shop list and subscriptions
                        candidates = [sh for sh in matches
                                      if (sh.phone in [su.shop_phone 
                                                       for su in subs])]
                        if len(candidates) > 0:
                            # swap subscriptions to beginning of list
                            for match in candidates:
                                matches = ([match] + 
                                           matches[:matches.index(match)] + 
                                           matches[matches.index(match)+1:]) 
                    
                    # create a message of at most 160 characters (1 SMS)
                    for match in matches:
                        temp += (MSG_FOUND_SHOP_FOR_CATEGORY % 
                                 (match.name, match.address, match.status))
                        # include at least one result
                        if (len(temp.strip()) <= app_config.MAX_MSG_LENGTH
                            or reply == ''):
                            reply = temp.strip()
                        else:
                            logging.info('DONE: Shop find query')
                            break
                else:
                    logging.info('DONE: No shops found for query')
                    reply = MSG_NO_SHOPS_FOR_CATEGORY % (cust.name, category)
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
            logging.info('ERROR: Customer not registered')
            reply = MSG_CUST_NOT_REGISTERED
        else:
            # get all matching shops
            (shops, 
             location_estimate) = self.fetch_shops_to_subscribe(phone, 
                                                                shop_name, 
                                                                address)
            if shops == None:
                logging.info('ERROR: No shop found for subscription')
                reply = MSG_NO_SHOPS_FOR_NAME % cust.name
            elif len(shops) != 1:
                logging.info('ERROR: Many shops found for subscription')
                # say customer we found many matches
                reply = self.found_many_shops_msg(shops, location_estimate)
            else:
                # exactly 1 shop found
                cust_phone = cust.phone
                shop_phone = shops[0].phone
                
                try:
                    # check if already subscribed
                    if Subscription.exists(cust_phone, shop_phone):
                        logging.info('ERROR: Subscription exists')
                        reply = (MSG_ALREADY_SUBSCRIBED %
                                 (cust.name, shops[0].name))
                    else:
                        new_subs = Subscription(cust_phone=cust_phone,
                                                shop_phone=shop_phone,
                                                start_time=
                                                self.query.params['start_time']
                                                )
                        new_subs.persist()
                        logging.info('DONE: Subscription made')
                        reply = MSG_SUBSCRIBED_TO_SHOP % (cust.name, 
                                                          shops[0].name)
                except BaseException as e:
                    logging.error(e)
                    reply = MSG_ERROR
        return reply

    def check_shop_status(self):
        """ return status of subscribed shop(s): workflow """
        # check customer; proceed only if a registered customer
        shop_name = self.query.params['shop']
        phone = self.query.params['phone']
        
        cust = Customer.retrieve(phone)
        
        reply = None    # reply message
        
        if cust == None:    # respond with error if not registered
            logging.info('ERROR: Customer not registered')
            reply = MSG_CUST_NOT_REGISTERED
        else:
            # get all subscriptions of customer
            subs = Subscription.search_by_cust(cust.phone)
            if subs == None:
                # cannot proceed; no subscriptions
                logging.info('ERROR: No subscription found')
                reply = MSG_CUST_NOT_SUBSCRIBED % cust.name
            else:
                # get all matching shops
                shops = Shop.search_by_name(shop_name)
                if shops == None:
                    logging.info('ERROR: No shop found for status check')
                    reply = MSG_NO_SHOPS_FOR_NAME % cust.name
                else:
                    # get intersection of shop list and customer subscriptions
                    candidates = [sh for sh in shops
                                  if (sh.phone in [su.shop_phone 
                                                   for su in subs])]
                    if len(candidates) > 0:
                        # create a message of at most 160 characters (1 SMS)
                        reply = ''
                        temp = ''
                        
                        for match in candidates:
                            temp += (MSG_FOUND_SHOP_FOR_CATEGORY % 
                                     (match.name, match.address, match.status))
                            # include at least one result
                            if (len(temp.strip()) <= app_config.MAX_MSG_LENGTH
                                or reply == ''):
                                reply = temp.strip()
                            else:
                                logging.info('DONE: Shop find query')
                                break
                        
                        # update last query time of queried subscriptions
                        time_now = util.current_time()
                        queried = [su for su in subs 
                                   if su.shop_phone in
                                   [sh.phone for sh in shops]]
                        for match in queried:
                            match.last_query = time_now
                            match.persist()
                    else:
                        # cannot proceed; no matching subscriptions
                        logging.info('ERROR: No subscription found for shop')
                        reply = MSG_CUST_NOT_SUBSCRIBED_FOR_SHOP % (cust.name, 
                                                                    shop_name)
        return reply

    def untrack_shop(self):
        """ unsubscribe customer from given shop: workflow """
        # check customer; proceed only if a registered customer
        shop_name = self.query.params['shop']
        address = self.query.params['address']
        phone = self.query.params['phone']
        
        cust = Customer.retrieve(phone)
        
        reply = None    # reply message
        
        if cust == None:    # respond with error if not registered
            logging.info('ERROR: Customer not registered')
            reply = MSG_CUST_NOT_REGISTERED
        else:
            # get all subscriptions of customer
            subs = Subscription.search_by_cust(cust.phone)
            if subs == None:
                # cannot unsubscribe; no subscriptions
                logging.info('ERROR: No subscription found')
                reply = MSG_CUST_NOT_SUBSCRIBED % cust.name
            else:
                # get all matching shops
                (shops, 
                 location_estimate) = self.fetch_shops_to_subscribe(phone, 
                                                                    shop_name, 
                                                                    address)
                if shops == None:
                    logging.info('ERROR: No shop found for unsubscription')
                    reply = MSG_NO_SHOPS_FOR_NAME % cust.name
                else:
                    # get intersection of shop list and customer subscriptions
                    candidates = [su for su in subs 
                                  if su.shop_phone in
                                  [sh.phone for sh in shops]]
                    
                    if len(candidates) > 1:
                        # say customer we found many matches
                        logging.info('ERROR: Multiple subscriptions '
                                     'found for unsubscription')
                        reply = self.found_many_shops_msg(shops, 
                                                          location_estimate)
                    elif len(candidates) == 0:
                        # cannot unsubscribe; no matching subscriptions
                        logging.info('ERROR: No subscription found for shop')
                        reply = MSG_CUST_NOT_SUBSCRIBED_FOR_SHOP % (cust.name, 
                                                                    shop_name)
                    else:
                        # exactly 1 shop found
                        try:
                            # delete subscription
                            shop_phone = candidates[0].shop_phone 
                            candidates[0].delete()
                            logging.info('DONE: Unsubscribed from shop')
                            reply = (MSG_UNSUBSCRIBED_FROM_SHOP
                                     % (cust.name, [sh for sh in shops 
                                        if (sh.phone == shop_phone)][0].name))
                        except BaseException as e:
                            logging.error(e)
                            reply = MSG_ERROR
        return reply

    def unregister_cust(self):
        """ customer registration workflow """
        # check for customer in database; proceed only if present
        phone = self.query.params['phone']
        cust = Customer.retrieve(phone)
        
        reply = None    # reply message
        
        if cust == None:    # respond with error if not registered
            logging.info('ERROR: Customer not registered')
            reply = MSG_CUST_NOT_REGISTERED
        else:   # unregister, and confirm
            try:
                cust.delete()
                logging.info('DONE: Customer unregistered')
                reply = MSG_GOODBYE % cust.name
            except BaseException as e:
                logging.error(e)
                reply = MSG_ERROR
        return reply
    
    def unregister_shop(self):
        """ shop registration workflow """
        # check for shop in database; proceed only if present
        phone = self.query.params['phone']
        shop = Shop.retrieve(phone)
        
        reply = None    # reply message
        
        if shop == None:    # respond with error if not registered
            logging.info('ERROR: Shop not registered')
            reply = MSG_SHOP_NOT_REGISTERED
        else:   # unregister, and confirm
            try:
                shop.delete()
                logging.info('DONE: Shop unregistered')
                reply = MSG_GOODBYE % shop.name
            except BaseException as e:
                logging.error(e)
                reply = MSG_ERROR
        return reply
    
    """ Helper methods """
    
    def found_many_shops_msg(self, shops, location_estimate=False):
        """ generates message for multiple shop search results """
        # create a message of at most 160 characters (1 SMS)
        temp = MSG_FOUND_MANY_SHOPS % ''
        reply = ''
        
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
            if (len(temp.strip()) <= app_config.MAX_MSG_LENGTH
                or reply == ''):
                reply = temp.strip()
            else:
                return reply
            
    def fetch_shops_to_subscribe(self, cust_phone, shop_name, address=None):
        """ fetches shops based on provided parameters
            and customer location, if required """
        shops = None
        
        # did we use customer's location to find the shop?
        location_estimate = False
        
        # search by address (if available)
        if address != None: 
            shops = Shop.search_by_name(name=shop_name, address=address)
        else:
            logging.info('INFO: Address not found for subscription,'
                         ' trying location')
            location_estimate = True
            location = lbs_handler.request(cust_phone)
            shops = Shop.search_by_name(name=shop_name, location=location)
        
        return (shops, location_estimate)
