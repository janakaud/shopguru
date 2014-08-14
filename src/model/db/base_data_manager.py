'''
Created on Aug 9, 2014

@author: janaka
'''
from abc import ABCMeta, abstractmethod


class BaseDataManager:
    '''
    This class represents an abstract data manager interface.
    '''

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_instance(self):
        pass

    @abstractmethod
    def update_record(self, table, fields, values):
        pass

    @abstractmethod
    def insert_record(self, table, fields, values):
        pass