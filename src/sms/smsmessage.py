'''
Created on Aug 9, 2014

@author: janaka
'''

class SMSMessage:
    '''
    This class represents an SMS message in the application logic perspective.
    '''


    def __init__(self, phone, time, content):
        '''
        Constructor
        '''
        self.phone = phone;
        self.time = time;
        self.content = content;


    def __str__(self):
        text= 'Message ['
        text += 'phone: ' + self.phone + ', '
        text += 'time: ' + str(self.time) + ', '
        text += 'content: ' + self.content + ']'
        return text
    