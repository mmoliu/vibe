#main.py
import webapp2  #gives access to Google's deployment code
import jinja2
import os
from models import Person
import operator
#libraries for api_version
from google.appengine.api import urlfetch
import json



#This initializes the jinja2 environment
#TEMPLATE CODE FOR APPS / boiler plate code
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def percentMatch(user, person):
    simScore = 0
    lppl = Person._properties
    for attr in lppl:
        if getattr(user, attr) == getattr(person, attr):
            simScore += 1
    return simScore

#getVibing
def getVibes(user):
    person_query= Person.query().fetch()
    similarityIndex = {}
    for person in person_query:
        similarityIndex[str(person.fName) + " " + str(person.lName)] = percentMatch(user, person)
    sortedSimIndex = sorted(similarityIndex.items(), key=operator.itemgetter(1))
    return sortedSimIndex #returns a dictionary with the keys sorted by its value



#handler section
class HomePage(webapp2.RequestHandler):
    #request handler is the parent
    #gives us access that everything webapp has in its code

    def get(self): #request of getting stuff from a website
        home_dict={
        }
        welcome_template = jinja_env.get_template("html/main.html")
        self.response.write(welcome_template.render(home_dict)) #render takes in the jinja dict


class Vibe(webapp2.RequestHandler):
    def get(self):
        vibe_template = jinja_env.get_template("/html/vibe.html")
        self.response.write(vibe_template.render())


class ResultPage(webapp2.RequestHandler):
    def post(self):
        firstName = self.request.get("fname")
        lastName = self.request.get("lname")
        favColor = self.request.get("color") #if u only have this line, does not go back to page
        trueColor = self.request.get("TrueColor")
        favActivity = self.request.get("activity")
        music = self.request.get("music")
        user = Person(fName = firstName, lName = lastName, color= favColor, trueColor= trueColor, activity= favActivity, music=music)
        vibesList= getVibes(user) #list of tuples in order that have ppl's name, and similarity index
        user.put()

        data_dict = {
            "top_one": vibesList[0],
            "x" : (vibesList[0][1]/6)
        }

        result_template = jinja_env.get_template("/html/results.html")
        self.response.write(result_template.render(data_dict))

class DiscussionPage(webapp2.RequestHandler):
    def post(self):
        



#initialization
app = webapp2.WSGIApplication(
    [
    ('/', HomePage),
    ('/result', ResultPage),
    ('/vibe', Vibe),
    ('/discussion', DiscussionPage)
    ], debug = True

    #when you load up your application, and it ends w slash, this class should be handling all requests
    #reason it is an array is bc u can add others too
)
