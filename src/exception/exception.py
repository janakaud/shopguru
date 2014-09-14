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


class NameTooShortException(QueryException):
    def __str__(self):
        return 'ERROR: Name string too short'


class NameTooLongException(QueryException):
    def __str__(self):
        return 'ERROR: Name string too long'


class ActualNameTooShortException(NameTooShortException):
    def __str__(self):
        return 'ERROR: Persistent name string too short'


class ActualNameTooLongException(NameTooLongException):
    def __str__(self):
        return 'ERROR: Persistent name string too long'


class QueryNameTooShortException(NameTooShortException):
    def __str__(self):
        return 'ERROR: Query name string too short'


class QueryNameTooLongException(NameTooLongException):
    def __str__(self):
        return 'ERROR: Query name string too long'


class AddressTooShortException(QueryException):
    def __str__(self):
        return 'ERROR: Address string too short'


class AddressTooLongException(QueryException):
    def __str__(self):
        return 'ERROR: Address string too long'


class ActualAddressTooShortException(AddressTooShortException):
    def __str__(self):
        return 'ERROR: Persistent address string too short'


class ActualAddressTooLongException(AddressTooLongException):
    def __str__(self):
        return 'ERROR: Persistent address string too long'


class QueryAddressTooShortException(AddressTooShortException):
    def __str__(self):
        return 'ERROR: Query address string too short'


class QueryAddressTooLongException(AddressTooLongException):
    def __str__(self):
        return 'ERROR: Query address string too long'


class CategoryTooShortException(QueryException):
    def __str__(self):
        return 'ERROR: Category string too short'


class CategoryTooLongException(QueryException):
    def __str__(self):
        return 'ERROR: Category string too long'


class ActualCategoryTooShortException(CategoryTooShortException):
    def __str__(self):
        return 'ERROR: Persistent category string too short'


class ActualCategoryTooLongException(CategoryTooLongException):
    def __str__(self):
        return 'ERROR: Persistent category string too long'


class QueryCategoryTooShortException(CategoryTooShortException):
    def __str__(self):
        return 'ERROR: Query category string too short'


class QueryCategoryTooLongException(CategoryTooLongException):
    def __str__(self):
        return 'ERROR: Query category string too long'


class StatusException(QueryException):
    def __str__(self):
        return 'ERROR: Invalid status update'


class StatusTooShortException(StatusException):
    def __str__(self):
        return 'ERROR: Status too short'


class StatusTooLongException(StatusException):
    def __str__(self):
        return 'ERROR: Status too long'


class UnregistrationException(QueryException):
    def __str__(self):
        return 'ERROR: Invalid unregistration query'


class EntityException(ShopGuruException):
    def __str__(self):
        return 'ERROR: Invalid entity operation'


class EntityNotPersistedException(EntityException):
    def __str__(self):
        return 'ERROR: Attempt to manipulate nonpersistent entity'