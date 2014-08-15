'''
@author: janaka

This module maps entities from the application into data records
in the persistent storage.
'''

from db.mysql_data_manager import MySQLDataManager

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


def persist_customer(customer):
    """ persists Customer entity """
    if customer.persisted == False:  # not in storage; create new record
        get_manager().insert_record('customer',
                                    ['name', 'phone', 'reg_time',
                                     'latitude', 'longitude'],
                                    [customer.name, customer.phone,
                                     customer.reg_time,
                                     customer.location.latitude,
                                     customer.location.longitude])
    else:   # already in storage; update possible fieles of existing record
        get_manager().update_record('customer',
                                    ['phone'], [customer.phone],
                                    ['latitude', 'longitude'],
                                    [customer.location.latitude,
                                     customer.location.longitude])


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
    if result.rowcount > 0:
        # create Customer object from first retrieval 
        data = result.fetchone()
        return Customer(phone=phone,
                        name=data[0],
                        reg_time=data[1],
                        location=Location(data[2], data[3]),
                        persisted=True)
    else:
        return None
    

def persist_shop(shop):
    """ persists Shop entity """
    if shop.persisted == False:  # not in storage; create new record
        get_manager().insert_record('shop',
                                    ['name', 'phone', 'address', 'category', 
                                     'reg_time', 'latitude', 'longitude'],
                                    [shop.name, shop.phone, shop.address, 
                                     shop.category, shop.reg_time,
                                     shop.location.latitude,
                                     shop.location.longitude])
    else:   # already in storage; update possible fieles of existing record
        get_manager().update_record('shop',
                                    ['phone'], [shop.phone],
                                    ['latitude', 'longitude'],
                                    [shop.location.latitude,
                                     shop.location.longitude])


def retrieve_shop(phone):
    """ retrieves any Shops stored under given phone """
    # deferred import to circumvent circular dependency
    from model.entity.location import Location
    from model.entity.shop import Shop
    
    # return first record found, None otherwise
    result = get_manager().search_record('shop',
                                         ['name', 'address', 'category',
                                          'reg_time',
                                          'latitude', 'longitude'],
                                         ['phone'], [phone])
    if result.rowcount > 0:
        # create Shop object from first retrieval 
        data = result.fetchone()
        return Shop(phone=phone,
                    name=data[0],
                    address=data[1],
                    category=data[2],
                    reg_time=data[3],
                    location=Location(data[4], data[5]),
                    persisted=True)
    else:
        return None