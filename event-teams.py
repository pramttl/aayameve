import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.api import mail

from google.appengine.ext.webapp.util import run_wsgi_app

# Models is a User Defined Python File containing the Datastore Models for this application.
from models import *

from google.appengine.ext import db

import os
from google.appengine.ext.webapp import template

class EventUsers(webapp.RequestHandler):
    def get(self):
        events_query = Event.all().order("event")
        events = events_query.fetch(40)
        template_values = {
            'events':events
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/event-teams.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        event_selected = self.request.get()
        teams = Team.gql("WHERE event = :1",str(event_selected))
        
        template_values = {
            'event_selected':event_selected
            'teams':teams
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/event-teams2.html')
        self.response.out.write(template.render(path, template_values))


# Code to instantiate an application object, with a list of the mappings from the URL to the corresponding HANDLER CLASS.
application = webapp.WSGIApplication([
    (r'^(/event-teams)(.*)$', EventUsers),  
    (r'^(/event-teams2)(.*)$', EventUsers),  
], debug=True)

def main():
    run_wsgi_app(application) # Boilerplate, Code to run the application object.

if __name__ == '__main__':
    main()
