import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.api import users
from google.appengine.ext import webapp
import appengine_admin

from google.appengine.ext.webapp.util import run_wsgi_app

# Models is a User Defined Python File containing the Datastore Models for this application.
from models import *

from google.appengine.ext import db

import os
from google.appengine.ext.webapp import template
from sessions import gmemsess

class MainPage(webapp.RequestHandler):

    user = users.get_current_user()
    login_url = users.create_login_url("/")
    logout_url = users.create_logout_url("/")

    def get(self):
        events_query = Event.all().order("event")
        events = events_query.fetch(20)

        user = users.get_current_user()
        login_url = users.create_login_url("/")
        logout_url = users.create_logout_url("/")

        template_values = {
            'events': events,
            'user':user,
            'login_url': login_url,
            'logout_url': logout_url,
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, template_values))

    # Now since the user has selected his event, he has to create a team.
    def post(self):
        sess = gmemsess.Session(self)
        event_selected = self.request.get('event_selected')

        # Start a new session, if there are no old session variables, for the requesting user.
        if sess.is_new():
            selected_event = event_selected
            sess['event_selected'] = event_selected      
            sess.save()

            numrange = range(1,6)

            template_values = {
                'event_selected': event_selected,
                'user':self.user,
                'login_url': self.login_url,
                'logout_url': self.logout_url,
                'numrange': numrange,
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/team-registration.html')
            self.response.out.write(template.render(path, template_values))

        else:
            team_obj = Team()
            teamname_entered = self.request.get('team')
            user_email_list=[ str(self.request.get('member1')),
                              str(self.request.get('member2')),
                              str(self.request.get('member3')),
                              str(self.request.get('member4')),
                              str(self.request.get('member5'))]

            team_obj.team = teamname_entered #Assigning the value of teamname entered to team property of the entity.
            
            selected_event = sess['event_selected']
            sess.invalidate()

            #events_selected = Event.gql("WHERE event = :1",str(event_selected))
            event_selected_obj = Event.all().filter("event =",selected_event).get() # get() method is used on a Query object having one entity to get that entity.

            team_obj.event = event_selected_obj.key()
            team_obj.put()

            user_objects = User.gql("WHERE email_id in :1",user_email_list)
            team_entity = Team.gql("WHERE team = :1",str(teamname_entered)).get()

            for user_obj in user_objects:
                # Code to put a particular team in the a particular user's team list.            
                if team_entity.key() not in user_obj.team_list:
                    user_obj.team_list.append(team_entity.key())
                    user_obj.put()

            member_list = team_entity.members

            template_values = {
                'event_selected':selected_event,
                'user':self.user,
                'teamname': teamname_entered,
                'member_list': member_list,
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/registration-successful.html')
            self.response.out.write(template.render(path, template_values))


# Code to instantiate an application object, with a list of the mappings from the URL to the corresponding HANDLER CLASS.
application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/event-registration',MainPage),
    ('/team-registration',MainPage),
    # Admin pages
    (r'^(/admin)(.*)$', appengine_admin.Admin), 
], debug=True)

def main():
    run_wsgi_app(application) # Boilerplate, Code to run the application object.

if __name__ == '__main__':
    main()
