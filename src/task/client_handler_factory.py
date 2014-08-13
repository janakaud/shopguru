#!/usr/local/bin/python2.7
# encoding: utf-8
'''
test -- shortdesc

test is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2014 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

from clienthandler import ClientHandler

def new_client(message):
    handler = ClientHandler(message)
    return handler