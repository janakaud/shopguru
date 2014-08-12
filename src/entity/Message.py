'''
Created on Aug 9, 2014

@author: janaka
'''

class Message(object):
    '''
    classdocs
    '''


    def __init__(self, sender, time, content):
        '''
        Constructor
        '''
        self.sender = sender;
        self.time = time;
        self.content = content;


    def display(self):
        print('Message')
        print('from: ' + self.sender)
        print('at: ' + self.time)
        print('content: ' + self.content)
    