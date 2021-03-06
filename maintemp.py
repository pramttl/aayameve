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
from sessions import gmemsess # Session Library using google "memcached" for data storage, which is not a good option, when perfect transaction is required.
from google.appengine.ext.db import djangoforms

class UserRegistrationForm(djangoforms.ModelForm):
    class Meta:
        model = User
        exclude = ['email_id','date','team_list','team_list_viewable']

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        login_url = users.create_login_url("/")
        logout_url = users.create_logout_url("/")

        template_values = {
            'user':user,
            'login_url': login_url,
            'logout_url': logout_url,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, template_values))

class UserRegistration(webapp.RequestHandler):
    def get(self):

        user = users.get_current_user()
        user_email = str(user.email())
        login_url = users.create_login_url("/")
        logout_url = users.create_logout_url("/")

        user_object = User.all().filter("email_id =",user_email).get()
        if user_object == None:
            user_already_registered = False
        else:
            user_already_registered = True

        user_registration_form = UserRegistrationForm()
        template_values = {
            'user':user,
            'login_url': login_url,
            'logout_url': logout_url,
            'user_registration_form':user_registration_form,
            'user_already_registered': user_already_registered,
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/user-registration.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        data = UserRegistrationForm(data=self.request.POST)

        user = users.get_current_user()
        login_url = users.create_login_url("/")
        logout_url = users.create_logout_url("/")

        if data.is_valid():
            ## Save the data, and redirect to the view page
            entity = data.save(commit=False)
            entity.email_id = str(users.get_current_user().email())
            entity.put()

            template_values = {
                'user':user,
                'login_url': login_url,
                'logout_url': logout_url,
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/user-registered.html')
            self.response.out.write(template.render(path, template_values))
        else:
            ## Reprint the form
            self.redirect("/user-registration")

## Code very repetitive to the User Registration Code, but the earlier implementation was based on ModelForms.
'''
class UserProfile(webapp.RequestHandler):
    def get(self):
        save_success = False
        user = users.get_current_user()
        user_email = str(user.email())
        login_url = users.create_login_url("/")
        logout_url = users.create_logout_url("/")

        user_obj = User.all().filter("email_id =",user_email).get()
        if user_object == None:
            user_already_registered = False
        else:
            user_already_registered = True

        template_values = {
            'user':user,
            'login_url': login_url,
            'logout_url': logout_url,
            'user_obj':user_obj,
            'user_already_registered':user_already_registered,
            'save_success':save_success,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/user-profile.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        save_success = False
        user = users.get_current_user()
        user_email = str(user.email())
        login_url = users.create_login_url("/")
        logout_url = users.create_logout_url("/")

        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        gender = self.request.get('gender')
        mobile_number = self.request.get('mobile_number')
        college = self.request.get('college')

        user_obj = User.all().filter("email_id =",user_email).get()

        (user_obj.first_name,user_obj.last_name,user_obj.gender,user_obj.mobile_number,user_obj.college) = (first_name,last_name,gender,mobile_number,college)
        user_obj.put()
        save_success = True

        template_values = {
            'user':user,
            'login_url': login_url,
            'logout_url': logout_url,
            'user_obj':user_object,
            'save_success':save_success,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/user-profile.html')
        self.response.out.write(template.render(path, template_values))
'''

class EventRegistration(webapp.RequestHandler):
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

        path = os.path.join(os.path.dirname(__file__), 'templates/aayam-events.html')
        self.response.out.write(template.render(path, template_values))

class TeamRegistration(webapp.RequestHandler):
    # Now since the user has selected his event, he has to create a team.
    def post(self):
        sess = gmemsess.Session(self)
        event_selected = self.request.get('event_selected')

        user = users.get_current_user()
        login_url = users.create_login_url("/")
        logout_url = users.create_logout_url("/")

        ## Start a new session, if there are no old session variables, for the requesting user.
        if sess.is_new():
            event_selected = self.request.get('event_selected')

            # If someone is just accessing the event-page posting null values then don't run the script.
            sess['pageflag'] = 0

            if (event_selected != None and sess['pageflag'] == 0):
                selected_event = event_selected
                sess['event_selected'] = event_selected

                #To indicate that the Team URL has been accessed once.
                sess['pageflag'] = 1

                sess.save()

                numrange = range(1,6)

                template_values = {
                    'event_selected': event_selected,
                    'user': user,
                    'login_url': login_url,
                    'logout_url': logout_url,
                    'numrange': numrange,
                }
                path = os.path.join(os.path.dirname(__file__), 'templates/team-registration.html')
                self.response.out.write(template.render(path, template_values))

        # This 2nd condition is run when the user selects his teamname & team-mebers & then submits.
        elif (sess['event_selected'] and sess['pageflag']):

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

            # events_selected = Event.gql("WHERE event = :1",str(event_selected))
            event_selected_obj = Event.all().filter("event =",selected_event).get() # get() method is used on a Query object having one entity to get that entity.

            team_obj.event = event_selected_obj.key()
            team_obj.put()

            user_objects = User.gql("WHERE email_id in :1",user_email_list)
            team_entity = Team.gql("WHERE team = :1",str(teamname_entered)).get()

            for user_obj in user_objects:
                # Code to put a particular team in the a particular user's team list.            
                if team_entity.key() not in user_obj.team_list:
                    user_obj.team_list.append(team_entity.key())
                    user_obj.team_list_viewable.append(str(team_entity.team))
                    user_obj.put()

            member_query_list = team_entity.members

            # Code to register the team with the corresponding member_list to the database, for admins to view.
            member_list = []
            for member in member_query_list:
                member_list.append(str(member.email_id))
            team_obj.memberlist = member_list

            team_obj.put()

            template_values = {
                'event_selected':selected_event,
                'user':user,
                'teamname': teamname_entered,
                'member_list': member_query_list,
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/registration-successful.html')
            self.response.out.write(template.render(path, template_values))


# Code to instantiate an application object, with a list of the mappings from the URL to the corresponding HANDLER CLASS.
application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/user-registration', UserRegistration),
    #('/user-profile', UserProfile),
    ('/aayam-events',EventRegistration),
    ('/event-registration',TeamRegistration),
    ('/team-registration',TeamRegistration),
    # Admin pages
    (r'^(/admin)(.*)$', appengine_admin.Admin), 
], debug=True)

def main():
    user = users.get_current_user()
    login_url = users.create_login_url("/")
    logout_url = users.create_logout_url("/")
    run_wsgi_app(application) # Boilerplate, Code to run the application object.

if __name__ == '__main__':
    main()
