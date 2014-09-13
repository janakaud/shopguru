'''
@author: janaka

This module maps entities from the application into data records
in the persistent storage.
'''

from db.mysql_data_manager import MySQLDataManager
from exception.exception import EntityNotPersistedException

manager = None


def get_manager():
    """ singleton pattern to retrieve data manager instance """
    global manager
    if manager is None:
        manager = MySQLDataManager.get_instance()
    return manager


def persist_incoming_sms(message):
    """ message logs can only be inserted; so don't allow updates """
    if message.msg_id is None:  # not in storage; create new record
        get_manager().insert_record('incoming_sms',
                                    ['sender', 'receive_time', 'content'],
                                    [message.phone, message.time,
                                     message.content])
    else:
        pass
        #raise Error('Message already persisted')


def persist_outgoing_sms(message):
    """ message logs can only be inserted; so don't allow updates """
    if message.msg_id is None:  # not in storage; create new record
        get_manager().insert_record('outgoing_sms',
                                    ['receiver', 'send_time', 'content'],
                                    [message.phone, message.time,
                                     message.content])
    else:
        pass
        #raise Error('Message already persisted')


""" Customer entity handlers """

def persist_customer(a_cust):
    """ persists Customer entity """
    if a_cust.persisted == False:  # not in storage; create new record
        get_manager().insert_record('customer',
                                    ['name', 'phone', 'reg_time',
                                     'latitude', 'longitude'],
                                    [a_cust.name, a_cust.phone,
                                     a_cust.reg_time,
                                     a_cust.location.latitude,
                                     a_cust.location.longitude])
    else:   # already in storage; update possible fieles of existing record
        get_manager().update_record('customer',
                                    ['phone'], [a_cust.phone],
                                    ['latitude', 'longitude'],
                                    [a_cust.location.latitude,
                                     a_cust.location.longitude])


def retrieve_customer(phone):
    """ retrieves any Customers stored under given phone """
    # deferred import to circumvent circular dependency
    from model.entity.location import Location
    from model.entity.customer import Customer
    
    # return first record found, None otherwise
    result = get_manager().search_record('customer',
                                         ['name', 'reg_time',
                                          'latitude', 'longitude'],
                                         ['phone'], [phone])
    if len(result) > 0:
        # create Customer object from first retrieval 
        data = result[0]
        return Customer(phone=phone,
                        name=data[0],
                        reg_time=data[1],
                        location=Location(data[2], data[3]),
                        persisted=True)
    else:
        return None


def search_customer(filter_fields, filter_values):
    """ retrieves any Customers matching given criteria """
    # deferred import to circumvent circular dependency
    from model.entity.location import Location
    from model.entity.customer import Customer
    
    # return all records found, None otherwise
    result = get_manager().search_record('customer', 
                                         ['phone', 'name', 'reg_time',
                                          'latitude', 'longitude'],
                                         filter_fields, filter_values)
    if len(result) > 0:
        # create list of Customer objects from results
        output = []
        for data in result: 
            output.append(Customer(phone=data[0],
                                   name=data[1],
                                   reg_time=data[2],
                                   location=Location(data[3], data[4]),
                                   persisted=True))
        return output
    else:
        return None
    

""" Shop entity handlers """

def persist_shop(a_shop):
    """ persists Shop entity """
    # deferred import to circumvent circular dependency
    from entity import shop

    if a_shop.persisted == False:  # not in storage; create new record
        get_manager().insert_record('shop',
                                    ['name', 'phone', 'address', 'category', 
                                     'reg_time', 'latitude', 'longitude',
                                     'status', 'last_update', 'lifetime'],
                                    [a_shop.name, a_shop.phone, a_shop.address, 
                                     a_shop.category, a_shop.reg_time,
                                     a_shop.location.latitude,
                                     a_shop.location.longitude,
                                     a_shop.status, a_shop.last_update,
                                     a_shop.lifetime])
        # set persisted flag
        a_shop.persisted = True
    
    else:   # already in storage; update fields of existing record
        if a_shop.changes == shop.DETAIL_CHANGED:  # update details
            get_manager().update_record('shop',
                                        ['phone'], [a_shop.phone],
                                        ['name', 'category'],
                                        [a_shop.name, a_shop.category])
        elif a_shop.changes == shop.LOCATION_CHANGED:  # update location
            get_manager().update_record('shop',
                                        ['phone'], [a_shop.phone],
                                        ['latitude', 'longitude'],
                                        [a_shop.location.latitude,
                                         a_shop.location.longitude])
        elif a_shop.changes == shop.STATUS_CHANGED:    # update status
            get_manager().update_record('shop',
                                        ['phone'], [a_shop.phone],
                                        ['status', 'last_update'],
                                        [a_shop.status, a_shop.last_update])
        # clear modified flag
        a_shop.changes = None


def retrieve_shop(phone):
    """ retrieves any Shops stored under given phone """
    # deferred import to circumvent circular dependency
    from model.entity.location import Location
    from model.entity.shop import Shop
    
    # return first record found, None otherwise
    result = get_manager().search_record('shop',
                                         ['name', 'address', 'category',
                                          'reg_time', 'latitude', 'longitude',
                                          'status', 'last_update', 'lifetime'],
                                         ['phone'], [phone])
    if len(result) > 0:
        # create Shop object from first retrieval 
        data = result[0]
        return Shop(phone=phone,
                    name=data[0],
                    address=data[1],
                    category=data[2],
                    reg_time=data[3],
                    location=Location(data[4], data[5]),
                    status=data[6],
                    last_update=data[7],
                    lifetime=data[8],
                    persisted=True)
    else:
        return None


def search_shop(filter_fields, filter_values,
                order_fields=None, order_values=None, search_with_like=False):
    """ retrieves any Shops matching given criteria """
    # deferred import to circumvent circular dependency
    from model.entity.location import Location
    from model.entity.shop import Shop
    
    # return all records found, None otherwise
    result = get_manager().search_record('shop', 
                                         ['phone', 'name', 'address',
                                          'category', 'reg_time',
                                          'latitude', 'longitude', 'status',
                                          'last_update', 'lifetime'],
                                         filter_fields, filter_values,
                                         order_fields, order_values,
                                         search_with_like)
    if len(result) > 0:
        # create list of Shop objects from results
        output = []
        for data in result: 
            output.append(Shop(phone=data[0],
                               name=data[1],
                               address=data[2],
                               category=data[3],
                               reg_time=data[4],
                               location=Location(data[5], data[6]),
                               status=data[7],
                               last_update=data[8],
                               lifetime=data[9],
                               persisted=True))
        return output
    else:
        return None


""" Subscription entity handlers """

def persist_subscription(a_subs):
    """ persists Subscription entity """
    if a_subs.persisted == False:  # not in storage; create new record
        get_manager().insert_record('subscription',
                                    ['cust_phone', 'shop_phone', 'start_time',
                                     'last_query'],
                                    [a_subs.cust_phone, a_subs.shop_phone,
                                     a_subs.start_time, a_subs.last_query])
    else:   # already in storage; update possible fieles of existing record
        get_manager().update_record('subscription',
                                    ['cust_phone', 'shop_phone'], 
                                    [a_subs.cust_phone, a_subs.shop_phone],
                                    ['last_query'], [a_subs.last_query])


def retrieve_subscription(cust_phone, shop_phone):
    """ retrieves any Subscriptions with given phone numbers """
    # deferred import to circumvent circular dependency
    from model.entity.location import Location
    from model.entity.subscription import Subscription
    
    # return first record found, None otherwise
    result = get_manager().search_record('subscription',
                                         ['start_time', 'last_query'],
                                         ['cust_phone', 'shop_phone'], 
                                         [cust_phone, shop_phone])
    if len(result) > 0:
        # create Subscription object from first retrieval 
        data = result[0]
        return Subscription(cust_phone=cust_phone,
                            shop_phone=shop_phone,
                            start_time=data[0],
                            last_query=data[1],
                            persisted=True)
    else:
        return None


def delete_subscription(a_subs):
    """ persists Subscription entity """
    if a_subs.persisted == True:  # not in storage; create new record
        get_manager().delete_record('subscription',
                                    ['cust_phone', 'shop_phone'],
                                    [a_subs.cust_phone, a_subs.shop_phone])
    else:   # already in storage; update possible fieles of existing record
        raise EntityNotPersistedException


def search_subscription(filter_fields, filter_values):
    """ retrieves any Subscriptions matching given criteria """
    # deferred import to circumvent circular dependency
    from model.entity.location import Location
    from model.entity.subscription import Subscription
    
    # return all records found, None otherwise
    result = get_manager().search_record('subscription', 
                                         ['cust_phone', 'shop_phone', 'start_time',
                                          'last_query'],
                                         filter_fields, filter_values)
    if len(result) > 0:
        # create list of Subscription objects from results
        output = []
        for data in result: 
            output.append(Subscription(cust_phone=data[0],
                                       shop_phone=data[1],
                                       start_time=data[2],
                                       last_query=data[3],
                                       persisted=True))
        return output
    else:
        return None