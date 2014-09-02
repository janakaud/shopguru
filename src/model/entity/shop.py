'''
@author: janaka
'''

from model import entity_manager
from base_entity import BaseEntity


class Shop(BaseEntity):
    '''
    This class represents a Shop (shop detail provider) of the application.
    '''

    def __init__(self, name, phone, address, category,
                 reg_time, location, persisted=False):
        """ initialize a new Shop """
        self.phone = phone
        self.name = name
        self.address = address
        self.reg_time = reg_time
        self.category = category
        self.location = location
        self.persisted = persisted  # indicates if already written to storage
    
    def persist(self):
        """ persist current Shop entity data in storage """
        entity_manager.persist_shop(self)
    
    @classmethod
    def retrieve(cls, phone):
        """ retrieve Shop (if any) with given phone number """
        return entity_manager.retrieve_shop(phone)
    
    @classmethod
    def exists(cls, phone):
        """ see if a Shop exists under given phone number """
        return (cls.retrieve(phone) != None)