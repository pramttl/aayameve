from google.appengine.ext import db
import appengine_admin

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
    college = db.PostalAddressProperty()
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
    readonlyFields = ('team_list_viewable','date',)

# Register to admin site
appengine_admin.register(AdminEvent,AdminTeam,AdminUser)
