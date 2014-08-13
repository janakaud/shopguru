'''
Created on Aug 9, 2014

@author: janaka
'''

from sms.smsreceiver import SMSReceiver
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp

app = webapp.WSGIApplication([('/receive', SMSReceiver)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()