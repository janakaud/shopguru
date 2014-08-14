'''
Created on Aug 13, 2014

@author: janaka

This module maps entities from the application into data records
in the persistent storage.
'''

from db.mysql_data_manager import MySQLDataManager

manager = None


def get_manager():
    global manager
    if manager is None:
        manager = MySQLDataManager.get_instance()
    return manager


def persist_incoming_sms(self, message):
    if message.msg_id is None:  # not in storage; create new record
        get_manager().insert_record('incoming_sms',
                                    ['sender', 'receive_time', 'content'],
                                    [message.phone, message.time,
                                     message.content])


def persist_outgoing_sms(self, message):
    if message.msg_id is None:  # not in storage; create new record
        get_manager().insert_record('outgoing_sms',
                                    ['receiver', 'send_time', 'content'],
                                    [message.phone, message.time,
                                     message.content])
