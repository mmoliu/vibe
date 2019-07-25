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
    sortedSimIndex = sorted(similarityIndex.items(), key=operator.itemgetter(1), reverse=True)
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
            "top_one": vibesList[1][0],
            #"lenVibes": len(vibesList[0][1]),
            "vibesList": getVibes(user),
            "x1": str(round(((float((vibesList[1][1])*100))/6),2)),
            "second":  vibesList[2][0],
            "x2": str(round(((float((vibesList[1][1])*100))/6),2)),
            "third":  vibesList[3][0],
            "x3": str(round(((float((vibesList[1][1])*100))/6),2)),
            "fourth":  vibesList[4][0],
            "x4": str(round(((float((vibesList[1][1])*100))/6),2)),

            "bottom": vibesList[len(vibesList)-1][0],
            "x5": str(round(((float((vibesList[len(vibesList)-1][1])*100))/6),2)),
            "secondBot":vibesList[len(vibesList)-2][0],
            "x6": str(round(((float((vibesList[len(vibesList)-2][1])*100))/6),2)),
            "thirdBot":vibesList[len(vibesList)-3][0],
            "x7": str(round(((float((vibesList[len(vibesList)-3][1])*100))/6),2)),
            "fourthBot":vibesList[len(vibesList)-4][0],
            "x8": str(round(((float((vibesList[len(vibesList)-4][1])*100))/6),2))

        }

        result_template = jinja_env.get_template("/html/results.html")
        self.response.write(result_template.render(data_dict))

class Video(webapp2.RequestHandler):
    def get(self):
        video_template = jinja_env.get_template("/html/video.html")
        self.response.write(video_template.render())



#initialization
app = webapp2.WSGIApplication(
    [
    ('/', HomePage),
    ('/result', ResultPage),
    ('/vibe', Vibe),
    ('/video', Video)
    ], debug = True

    #when you load up your application, and it ends w slash, this class should be handling all requests
    #reason it is an array is bc u can add others too
)
