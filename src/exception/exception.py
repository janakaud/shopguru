'''
@author: janaka

Defines the error hierarchy used in the application
'''

class ShopGuruException(Exception):
    def __str__(self):
        return 'ShopGuruException'


class QueryException(ShopGuruException):
    def __str__(self):
        return 'Invalid user query'


class RegistrationException(QueryException):
    def __str__(self):
        return 'Invalid registration query'


class MissingDetailsException(RegistrationException):
    def __str__(self):
        return 'Details not provided in registration query'


class MissingNameException(RegistrationException):
    def __str__(self):
        return 'Name not provided in registration query'


class MissingShopCategoryException(RegistrationException):
    def __str__(self):
        return 'Name not provided in registration query'