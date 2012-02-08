from google.appengine.ext import db
import appengine_admin

## This module is a ditto copy of appengine_admin but just to create another admin panel with less powers. Just a make do way.
import aayam_admin

class Event(db.Model):
    """The model for an Event of the festival"""
    event = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

    def __unicode__(self):
        return self.event

class Team(db.Model):
    """The model for an Event of the festival"""
    team = db.StringProperty()
    event = db.ReferenceProperty(Event)
    date = db.DateTimeProperty(auto_now_add=True)

    # member_list = db.ListProperty(db.Key)
    # Code to return a Gquel Object with the members of a particular team.
    @property
    def members(self):
        return User.gql("WHERE team_list = :1", self.key())
    
    memberlist = db.StringListProperty()

    def __unicode__(self):
        return self.team

class User(db.Model):
    """The model for an Event of the festival"""
    email_id = db.EmailProperty()
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    gender = db.StringProperty(choices=set(["M", "F"]))
    age = db.IntegerProperty()
    mobile_number = db.PhoneNumberProperty()
    college = db.PostalAddressProperty(verbose_name="College,City")
    date = db.DateTimeProperty(auto_now_add=True)

    team_list = db.ListProperty(db.Key) # Useful for creating a m2m relation b/n Team & User.
    team_list_viewable = db.StringListProperty() # An attribute, just for the admin users to view the teams of a user easily.

    def __unicode__(self):
        return self.email_id

## Admin views ##
class AdminEvent(appengine_admin.ModelAdmin):
    model = Event
    listFields = ('event', 'date')
    editFields = ('event',)
    readonlyFields = ('date',)

class AdminTeam(appengine_admin.ModelAdmin):
    model = Team
    listFields = ('team', u'event', 'date','memberlist')
    editFields = ('team', u'event','memberlist')
    readonlyFields = ('date',)

class AdminUser(appengine_admin.ModelAdmin):
    model = User
    listFields = ('first_name','last_name','gender','age','email_id','mobile_number','college','team_list_viewable','date')
    editFields = ('first_name','last_name','gender','age','email_id','mobile_number','college','team_list_viewable')
    readonlyFields = ('date',)

## Admin views ##
class AdminEvent2(appengine_admin.ModelAdmin):
    model = Event
    listFields = ('event', 'date')
    editFields = ('event',)
    readonlyFields = ('date',)

class AdminTeam2(appengine_admin.ModelAdmin):
    model = Team
    listFields = ('team', u'event', 'date','memberlist')
    editFields = ('team',)
    readonlyFields = (u'event', 'date','memberlist')

class AdminUser2(appengine_admin.ModelAdmin):
    model = User
    listFields = ('first_name','last_name','gender','age','email_id','mobile_number','college','team_list_viewable','date')
    editFields = ('first_name','last_name')
    readonlyFields = ('date','gender','age','email_id','mobile_number','college','team_list_viewable','date',)

# Register to admin site
appengine_admin.register(AdminEvent,AdminTeam,AdminUser)
aayam_admin.register(AdminEvent2,AdminTeam2,AdminUser2)
