'''
Created on Aug 13, 2014

@author: janaka
'''

from model import entity_manager
from base_entity import BaseEntity


class Subscription(BaseEntity):
    '''
    This class represents an association between a customer and a subscription. 
    '''

    def __init__(self, cust_phone, shop_phone, start_time, last_query=None,
                 persisted=False):
        """ initialize a new Subscription """
        self.cust_phone = cust_phone
        self.shop_phone = shop_phone
        self.start_time = start_time # indicates time of starting subscription
        self.last_query = last_query # indicates time of last query by customer
        self.persisted  = persisted
    
    def persist(self):
        """ persist current Subscription entity data in storage """
        entity_manager.persist_subscription(self)
    
    def delete(self):
        """ delete current Subscription entity data from storage """
        entity_manager.delete_subscription(self)
        
    @classmethod
    def retrieve(cls, cust_phone, shop_phone):
        """ retrieve Subscription (if any) with given phone number """
        return entity_manager.retrieve_subscription(cust_phone, shop_phone)
    
    @classmethod
    def exists(cls, cust_phone, shop_phone):
        """ see if a Subscription exists between given phone numbers """
        return (cls.retrieve(cust_phone, shop_phone) != None)
    
    @classmethod
    def search_by_cust(cls, cust_phone):
        """ retrieve all Subscriptions (if any) of given customer """
        return entity_manager.search_subscription(['cust_phone'], [cust_phone])