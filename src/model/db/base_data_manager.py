'''
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
        """ singleton method to return instance of current data manager """
        pass

    @abstractmethod
    def update_record(self, table,
                      filter_fields, filter_values,
                      fields, values):
        """ updates record(s) matching given field values, in given table """
        pass

    @abstractmethod
    def insert_record(self, table, fields, values):
        """ inserts record(s) with given field values, into given table """
        pass
    
    @abstractmethod
    def search_record(self, table, select_fields,
                      filter_fields, filter_values):
        """ searches for record(s) with given criteria, in given table """
        pass
