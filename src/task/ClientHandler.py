import threading;

'''
Created on Aug 8, 2014

@author: janaka
'''

class ClientHandler(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, message):
        '''
        Constructor
        '''
        self.message = message
    
    
    def run(self):
        self.message.display()