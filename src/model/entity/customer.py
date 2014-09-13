'''
@author: janaka
'''

from model import entity_manager
from base_entity import BaseEntity


class Customer(BaseEntity):
    '''
    This class represents a Customer (inquirer of shops) of the application.
    '''

    def __init__(self, name, phone, reg_time, location, persisted=False):
        """ initialize a new Customer """
        self.name = name
        self.reg_time = reg_time
        self.phone = phone
        self.location = location
        self.persisted = persisted  # indicates if already written to storage
    
    def persist(self):
        """ persist current Customer entity data in storage """
        entity_manager.persist_customer(self)
    
    def delete(self):
        """ delete current Customer entity data from storage """
        entity_manager.delete_customer(self)
    
    @classmethod
    def retrieve(cls, phone):
        """ retrieve Customer (if any) with given phone number """
        return entity_manager.retrieve_customer(phone)
    
    @classmethod
    def exists(cls, phone):
        """ see if a Customer exists under given phone number """
        return (cls.retrieve(phone) != None)