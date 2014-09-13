'''
@author: janaka

This module parses SMS text to generate a Query representing
a use case of the application.
'''

import re
from task import query
from task.query import Query
from exception.exception import *

# messaging formats - for reference
MSG_REG_SHOP = 'REG SHOP N:shop-name A:shop-address C:shop-category'
MSG_REG_CUST = 'REG CUST N:name A:address'
MSG_UNREG_SHOP = 'UNREG SHOP'
MSG_UNREG_CUST = 'UNREG CUST'


def parse(message):
    """ parser's control method """
    # convert message to lowercase and tokenize
    text = message.content
    tokens = re.split('\s', text, 1)
    tokens[0] = tokens[0].lower()
    
    # handle single-word queries
    if len(tokens) == 1:
        tokens.append('')
    
    # registration
    if tokens[0] == 'reg':
        return parse_reg(message, tokens[1])
    # category-based shop find - customer
    elif tokens[0] == 'find':
        return parse_find(message, tokens[1])
    # subscribed shop status - customer
    elif tokens[0] == 'status':
        return parse_check_status(message, tokens[1])
    # subscribing under given shop name - customer
    elif tokens[0] == 'track':
        return parse_track(message, tokens[1])
    # unsubscribing under given shop name - customer
    elif tokens[0] == 'untrack':
        return parse_untrack(message, tokens[1])
    # updating shop status - shop
    elif tokens[0] == 'update':
        return parse_update_status(message, tokens[1])
    # unregistration
    elif tokens[0] == 'unreg':
        return parse_unreg(message, tokens[1])
    else:
        raise QueryException()


def parse_reg(message, tokens):
    """ registration parser control method """
    tokens = re.split('\s', tokens.strip(), 1)
    tokens[0] = tokens[0].lower()
    
    # customer registration
    if(tokens[0] == 'cust'):
        return parse_reg_cust(message, tokens[1])
    # shop registration
    elif(tokens[0] == 'shop'):
        return parse_reg_shop(message, tokens[1])
    # undefined query
    else:
        raise RegistrationException()


def parse_reg_cust(message, tokens):
    """ customer registration parser """
    # user name
    try:
        token = re.search('[Nn]:.*', tokens).group(0)
        # eliminate other sections
        pos = re.search('[Aa]:', token)
        if pos != None:
            token = token[:pos.start()]
        name = str(token[2:len(token)]).strip()
    except AttributeError:
        raise MissingCustomerNameException()

    # address
    try:
        token = re.search('[Aa]:.*', tokens).group(0)
        # eliminate other sections
        pos = re.search('[Nn]:', token)
        if pos != None:
            token = token[:pos.start()]
        address = str(token[2:len(token)]).strip()
    except AttributeError:
        address = None
    
    if name != None:
        return Query(query.CUST_REGISTER,
                      dict(
                           name = name,
                           reg_time = message.time,
                           address = address,
                           phone = message.phone
                           )
                      )
    else:
        return None


def parse_reg_shop(message, tokens):
    """ shop registration parser """
    # shop name
    try:
        token = re.search('[Nn]:.*', tokens).group(0)
        # eliminate other sections
        pos = re.search('[AaCc]:', token)
        if pos != None:
            token = token[:pos.start()]
        name = str(token[2:len(token)]).strip()
    except AttributeError:
        raise MissingShopNameException()

    # address; if not provided in registration SMS,
    # keep address blank for next stage (LBS+geocode based location)
    try:
        token = re.search('[Aa]:.*', tokens).group(0)
        # eliminate other sections
        pos = re.search('[NnCc]:', token)
        if pos != None:
            token = token[:pos.start()]
        address = str(token[2:len(token)]).strip()
    except AttributeError:
        address = None

    # shop type
    try:
        token = re.search('[Cc]:.*', tokens).group(0)
        # eliminate other sections
        pos = re.search('[AaNn]:', token)
        if pos != None:
            token = token[:pos.start()]
        category = str(token[2:len(token)]).strip()
    except AttributeError:
        raise MissingShopCategoryException()
    
    if name != None:
        return Query(query.SHOP_REGISTER,
                      dict(
                           name = name,
                           reg_time = message.time,
                           address = address,
                           phone = message.phone,
                           category = category
                           )
                      )
    else:
        return None
    

def parse_find(message, category):
    """ shop finder parser """
    # shop finder (based on shop category)
    if category != None:
        return Query(query.FIND_SHOP,
                      dict(
                           category = category,
                           phone = message.phone
                           )
                      )
    else:
        return None
    
    
def parse_check_status(message, shop):
    """ shop status check parser """
    # shop status check (based on shop name)
    if shop != None:
        return Query(query.SHOP_STATUS,
                      dict(
                           shop = shop,
                           phone = message.phone
                           )
                      )
    else:
        return None


def parse_track(message, tokens):
    """ shop track parser """

    # shop name
    try:
        token = re.search('[Nn]:.*', tokens).group(0)
        # eliminate other sections
        pos = re.search('[AaCc]:', token)
        if pos != None:
            token = token[:pos.start()]
        name = str(token[2:len(token)]).strip()
    except AttributeError:
        name = tokens.strip()

    # address; if not provided in subscription SMS,
    # keep address blank for next stage (LBS+geocode based location)
    try:
        token = re.search('[Aa]:.*', tokens).group(0)
        # eliminate other sections
        pos = re.search('[NnCc]:', token)
        if pos != None:
            token = token[:pos.start()]
        address = str(token[2:len(token)]).strip()
    except AttributeError:
        address = None

    if name != None:
        return Query(query.TRACK_SHOP,
                      dict(
                           shop = name,
                           address = address,
                           start_time = message.time,
                           phone = message.phone
                           )
                      )
    else:
        return None


def parse_untrack(message, tokens):
    """ shop track stop parser """

    # shop name
    try:
        token = re.search('[Nn]:.*', tokens).group(0)
        # eliminate other sections
        pos = re.search('[AaCc]:', token)
        if pos != None:
            token = token[:pos.start()]
        name = str(token[2:len(token)]).strip()
    except AttributeError:
        name = tokens.strip()

    # address; if not provided in subscription SMS,
    # keep address blank for next stage (LBS+geocode based location)
    try:
        token = re.search('[Aa]:.*', tokens).group(0)
        # eliminate other sections
        pos = re.search('[NnCc]:', token)
        if pos != None:
            token = token[:pos.start()]
        address = str(token[2:len(token)]).strip()
    except AttributeError:
        address = None

    if name != None:
        return Query(query.UNTRACK_SHOP,
                      dict(
                           shop = name,
                           address = address,
                           phone = message.phone
                           )
                      )
    else:
        return None


def parse_update_status(message, status):
    """ shop status update parser """
    # shop track ('follow') (based on shop name)
    if status != None:
        return Query(query.UPDATE_STATUS,
                      dict(
                           status = status,
                           phone = message.phone
                           )
                      )
    else:
        return None


def parse_unreg(message, tokens):
    """ unregistration parser """
    tokens = re.split('\s', tokens.strip(), 1)
    user_type = tokens[0].lower()
    
    # customer unregistration
    if(user_type == 'cust'):
        return Query(query.CUST_UNREGISTER,
                      dict(
                           phone = message.phone
                           )
                      )
    # shop unregistration
    elif(user_type == 'shop'):
        return Query(query.SHOP_UNREGISTER,
                      dict(
                           phone = message.phone
                           )
                      )
    # undefined query
    else:
        raise UnregistrationException()
