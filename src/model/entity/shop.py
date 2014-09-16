'''
@author: janaka
'''

from model import entity_manager
from base_entity import BaseEntity
from config import util
from sms import sms_sender
from sms.message_parser import MSG_UPDATE_STATUS
from model.entity.message import OutgoingSMS
import logging

# possible types of changes the entity may undergo
DETAIL_CHANGED = 1
LOCATION_CHANGED = 2
STATUS_CHANGED = 3

MSG_REMIND_STATUS_UPDATE = ('Hello %s, your shop status has expired. '
                            'Please renew it by replying\n\n%s\n\n'
                            'Thank you!') % ('%s', MSG_UPDATE_STATUS)


class Shop(BaseEntity):
    '''
    This class represents a Shop (shop detail provider) of the application.
    '''

    def __init__(self, name, phone, address, category, reg_time, location,
                 status='?', last_update='', lifetime=24,
                 persisted=False, changes=None):
        """ initialize a new Shop """
        self.phone = phone
        self.name = name
        self.address = address
        self.reg_time = reg_time
        self.category = category
        self.location = location
        self.status = status
        self.last_update = last_update  # timestamp of last status update
        self.lifetime = lifetime    # lifetime of status update
        self.persisted = persisted  # indicates if already written to storage
        self.changes = changes      # indicates changes to be saved
    
    def persist(self):
        """ persist current Shop entity data in storage """
        entity_manager.persist_shop(self)
    
    def delete(self):
        """ delete current Customer entity data from storage """
        entity_manager.delete_shop(self)
    
    def check_status_expiry(self):
        """ check if Shop status expired, and notify the owner """
        try:
            if (self.status != '?' and 
                (self.last_update == None
                or util.get_delay(self.last_update) >= self.lifetime)):
                self.status = '?'   # sentinel for non-updated statuses
                self.changes = STATUS_CHANGED
                self.persist()
                
                # notify the shop owner to update his status
                logging.info('Reminding shop %s to update status' 
                             % str(self.phone))
                reply_sms = OutgoingSMS(self.phone, util.current_time(), 
                                        (MSG_REMIND_STATUS_UPDATE %
                                         self.name))
                sms_sender.send(reply_sms)
                reply_sms.persist()
        except BaseException as e:
            logging.error(e)
        
    @classmethod
    def retrieve(cls, phone):
        """ retrieve Shop (if any) with given phone number """
        result = entity_manager.retrieve_shop(phone)
        
        # check if shop status is expired; if so, remove it
        if result != None:
            result.check_status_expiry()
        
        return result
    
    @classmethod
    def exists(cls, phone):
        """ see if a Shop exists under given phone number """
        return (cls.retrieve(phone) != None)
    
    @classmethod
    def search_by_category(cls, location, category):
        """ retrieve the best matching shops of given category 
            around a given location """
        data = entity_manager.search_shop(['category'], ['%' + category + '%'],
                                          [('(POW(shop.latitude-%s, 2) + '
                                           'POW(shop.longitude-%s, 2))')],
                                          [location.latitude,
                                           location.longitude], True)
        
        # check if shop statuses is expired; if so, remove them
        if data != None:
            for a_shop in data: 
                a_shop.check_status_expiry()
        
        return data
        
    @classmethod
    def search_by_name(cls, name, address=None, location=None):
        """ retrieve the best matching shops of given name 
            around a given location or at a given address """
        data = None
        
        if address != None:
            # search by address
            data = entity_manager.search_shop(['name', 'address'],
                                              ['%' + name + '%',
                                               '%' + address + '%'],
                                              search_with_like=True)
        elif location != None:
            # search by address
            data = entity_manager.search_shop(['name'], ['%' + name + '%'],
                                              [('(POW(shop.latitude-%s, 2) + '
                                               'POW(shop.longitude-%s, 2))')],
                                              [location.latitude,
                                               location.longitude], True)
        else:
            # cannot filter by location; return result by name only
            data = entity_manager.search_shop(['name'], ['%' + name + '%'],
                                              search_with_like=True)
        
        # check if shop statuses is expired; if so, remove them
        if data != None:
            for a_shop in data: 
                a_shop.check_status_expiry()
        
        return data
