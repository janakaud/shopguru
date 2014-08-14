'''
Created on Aug 13, 2014

@author: janaka
'''

from model import entity_manager
from base_entity import BaseEntity


class Customer(BaseEntity):
    '''
    This class represents a Customer (inquirer of shops) of the application.
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
    
    def persist(self):
        entity_manager.persist_customer(self)