'''
@author: janaka
'''

from sms.sms_receiver import SMSReceiver
from config import app_config
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp

app = webapp.WSGIApplication([(app_config.SMS_SOURCE, SMSReceiver)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()