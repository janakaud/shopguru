'''
Created on Aug 12, 2014

@author: janaka
'''

CUST_REGISTER = 1
SHOP_REGISTER = 2

class Query:
    '''
    This class represents a user (customer/shop) query.
    '''
    
    type = None

    def __init__(self, type, params=None):
        '''
        params is a dictionary of parameters specific to the request type 
        identified by type parameter
        ''' 
        self.type = type
        self.params = params