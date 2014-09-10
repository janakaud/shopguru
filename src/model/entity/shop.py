'''
@author: janaka
'''

from model import entity_manager
from base_entity import BaseEntity

# possible types of changes the entity may undergo
DETAIL_CHANGED = 1
LOCATION_CHANGED = 2
STATUS_CHANGED = 3


class Shop(BaseEntity):
    '''
    This class represents a Shop (shop detail provider) of the application.
    '''

    def __init__(self, name, phone, address, category, reg_time, location,
                 status='', persisted=False, changes=None):
        """ initialize a new Shop """
        self.phone = phone
        self.name = name
        self.address = address
        self.reg_time = reg_time
        self.category = category
        self.location = location
        self.status = status
        self.persisted = persisted  # indicates if already written to storage
        self.changes = changes      # indicates changes to be saved
    
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
    
    @classmethod
    def search_by_category(cls, location, category):
        """ retrieve the best matching shops of given category 
            around a given location """
        return entity_manager.search_shop(['category'], [category],
                                          [('(POW(shop.latitude - %s, 2) + '
                                           'POW(shop.longitude - %s, 2))')],
                                          [location.latitude,
                                           location.longitude], True)