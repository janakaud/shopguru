'''
@author: janaka

Defines the error hierarchy used in the application
'''

class ShopGuruException(Exception):
    def __str__(self):
        return 'ERROR: ShopGuruException'


class QueryException(ShopGuruException):
    def __str__(self):
        return 'ERROR: Invalid user query'


class RegistrationException(QueryException):
    def __str__(self):
        return 'ERROR: Invalid registration query'


class MissingDetailsException(RegistrationException):
    def __str__(self):
        return 'ERROR: Details not provided in registration query'


class MissingNameException(RegistrationException):
    def __str__(self):
        return 'ERROR: Name not provided in registration query'


class MissingCustomerNameException(MissingNameException):
    def __str__(self):
        return 'ERROR: Name not provided in customer registration query'


class MissingShopNameException(MissingNameException):
    def __str__(self):
        return 'ERROR: Name not provided in shop registration query'


class MissingShopCategoryException(RegistrationException):
    def __str__(self):
        return 'ERROR: Category not provided in shop registration query'


class UnregistrationException(QueryException):
    def __str__(self):
        return 'ERROR: Invalid unregistration query'


class EntityException(ShopGuruException):
    def __str__(self):
        return 'ERROR: Invalid entity operation'


class EntityNotPersistedException(EntityException):
    def __str__(self):
        return 'ERROR: Attempt to manipulate nonpersistent entity'