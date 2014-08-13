'''
Created on Aug 9, 2014

@author: janaka
'''

from google.appengine.ext.webapp import RequestHandler

class WebappAdapter(RequestHandler):
    
    def __init__(self, *args):
        RequestHandler.__init__(self, *args)