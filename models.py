#where models will go
from google.appengine.ext import ndb
#import google.appengine.ext.db

class Person(ndb.Model):
    email = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    color = ndb.StringProperty(required=True)
    trueColor = ndb.StringProperty(required=True)
    activity = ndb.StringProperty(required=True)
    music = ndb.StringProperty(required=True)


class Message(ndb.Model):
    text = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
