'''
Created on Aug 13, 2014

@author: janaka
'''

from model import entity_manager
from base_entity import BaseEntity


class Shop(BaseEntity):
    '''
    This class represents a Shop (shop detail provider) of the application.
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
    
    def persist(self):
        entity_manager.persist_shop(self)
