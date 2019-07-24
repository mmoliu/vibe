#where models will go
from google.appengine.ext import ndb

class Person(ndb.Model):
    email = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    color = ndb.StringProperty(required=True)
    trueColor = ndb.StringProperty(required=True)
    activity = ndb.StringProperty(required=True)
    music = ndb.StringProperty(required=True)
