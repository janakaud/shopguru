from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
import SMSReceiver

application = webapp.WSGIApplication([('/receive', SMSReceiver)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()