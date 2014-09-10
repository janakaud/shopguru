'''
@author: janaka
'''

CUST_REGISTER = 1
SHOP_REGISTER = 2
FIND_SHOP = 3
SHOP_STATUS = 4
TRACK_SHOP = 5
UNTRACK_SHOP = 6
UPDATE_STATUS = 7
CUST_UNREGISTER = 8
SHOP_UNREGISTER = 9


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