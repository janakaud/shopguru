'''
Created on Aug 13, 2014

@author: janaka
'''

from model import entity_manager
from base_entity import BaseEntity


class Subscription(BaseEntity):
    '''
    This class 
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
    
    def persist(self):
        entity_manager.persist_subscription(self)