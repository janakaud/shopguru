'''
Created on Aug 9, 2014

@author: janaka
'''

from base_entity import BaseEntity
from model import entity_manager


class BaseSMS(BaseEntity):
    '''
    This class represents an abstract SMS message interface.
    '''

    def __init__(self, phone, time, content, msg_id=None):
        '''
        General-purpose constructor for SMS message
        If msg_id is None, message is not persisted yet
        '''
        self.phone = phone
        self.time = time
        self.content = content
        self.msg_id = msg_id

    def __str__(self):
        """ returns a textual representation of the message """ 
        text= 'Message ['
        text += 'phone: ' + str(self.phone) + ', '
        text += 'time: ' + str(self.time) + ', '
        text += 'content: ' + self.content + ']'
        return text


class IncomingSMS(BaseSMS):
    '''
    This class represents an SMS message received by the application
    '''

    def __init__(self, *args):
        BaseSMS.__init__(self, *args)

    def __str__(self):
        return 'Incoming' + BaseSMS.__str__(self)
    
    def persist(self):
        entity_manager.persist_incoming_sms(self)


class OutgoingSMS(BaseSMS):
    '''
    This class represents an SMS message sent out by the application
    '''

    def __init__(self, *args):
        BaseSMS.__init__(self, *args)

    def __str__(self):
        return 'Outgoing' + BaseSMS.__str__()
    
    def persist(self):
        entity_manager.persist_outgoing_sms(self)        