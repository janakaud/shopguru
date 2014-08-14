'''
@author: janaka
'''
from abc import ABCMeta, abstractmethod


class BaseEntity:
    '''
    Base class for all entities of application
    '''
    
    __metaclass__ = ABCMeta

    def __init__(self, params):
        pass

    @abstractmethod
    def persist(self):
        pass        