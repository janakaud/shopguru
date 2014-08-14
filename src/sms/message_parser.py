'''
Created on Aug 12, 2014

@author: janaka

This module parses SMS text to generate a Query representing
a use case of the application.
'''

import re
from task import query
from task.query import Query


def parse(message):
    # convert message to lowercase and tokenize
    text = message.content
    text = str(text).lower()
    tokens = re.split('\s', text, 1)
    
    msg_query = None
    
    # registration
    if tokens[0] == 'reg':
        tokens = re.split('\s', tokens[1].strip(), 1)
        
        # customer registration
        if(tokens[0] == 'cust'):
            # user name
            token = re.search('n:.*(\sa:)', text).group(0)
            name = str(token[2:len(token)-2]).strip()

            # address
            token = re.search('a:.*', text).group(0)
            address = str(token[2:]).strip()
            
            # get current coordinates if address unavailable
            # (needs LBS)
            if address == None:
                address = ''
            
            if name != None and address != None:
                msg_query = Query(query.CUST_REGISTER,
                              dict(
                                   name = name,
                                   reg_time = message.time,
                                   address = address,
                                   phone = message.phone
                                   )
                              )
    
    return msg_query