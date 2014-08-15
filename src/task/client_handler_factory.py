'''
@author: janaka

This module is a factory for client handlers which respond to
SMS queries/commands of users.
'''

from client_handler import ClientHandler


def new_client(message):
    """ creates and returns a new ClientHandler instance """
    handler = ClientHandler(message)
    return handler