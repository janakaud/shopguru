'''
@author: janaka

This module parses SMS text to generate a Query representing
a use case of the application.
'''

import re
from task import query
from task.query import Query
from src.exception.exception import RegistrationException, QueryException
from src.exception.exception import MissingNameException, MissingShopCategoryException


def parse(message):
    """ parser's control method """
    # convert message to lowercase and tokenize
    text = message.content
    text = str(text).lower()
    tokens = re.split('\s', text, 1)
    
    msg_query = None
    
    try:
        # registration
        if tokens[0] == 'reg':
            msg_query = parse_reg(message, tokens)
        else:
            raise QueryException()
    except IndexError:
        raise RegistrationException()
    
    return msg_query


def parse_reg(message, tokens):
    """ registration parser control method """
    tokens = re.split('\s', tokens[1].strip(), 1)
    
    # customer registration
    if(tokens[0] == 'cust'):
        return parse_reg_cust(message, tokens)
    # customer registration
    elif(tokens[0] == 'shop'):
        return parse_reg_shop(message, tokens)
    # undefined query
    else:
        raise QueryException()


def parse_reg_cust(message, tokens):
    """ customer registration parser """
    # user name
    try:
        token = re.search('n:.*(\sa:)', tokens[1]).group(0)
        name = str(token[2:len(token)-2]).strip()
    except AttributeError:
        raise MissingNameException()

    # address
    try:
        token = re.search('a:.*', tokens[1]).group(0)
        address = str(token[2:]).strip()
    except AttributeError:
        address = ''
    
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
        token = re.search('n:\s*.*(\sa:)', tokens[1]).group(0)
        name = str(token[2:len(token)-2]).strip()
    except AttributeError:
        raise MissingNameException()

    # address; if not provided in registration SMS,
    # keep address blank for next stage (LBS+geocode based location)
    try:
        token = re.search('a:\s*.*(\sc:)', tokens[1]).group(0)
        address = str(token[2:len(token)-2]).strip()
    except AttributeError:
        address = None

    # shop type
    try:
        token = re.search('c:\s*.*', tokens[1]).group(0)
        category = str(token[2:]).strip()
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