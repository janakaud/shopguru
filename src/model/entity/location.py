'''
@author: janaka
'''

class Location:
    '''
    Represents the geographical location (latitude, longitude)
    of an entity (shop/customer).
    '''

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        