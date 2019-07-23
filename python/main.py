#main.py
import webapp2  #gives access to Google's deployment code
import jinja2
import os
from models import Person

#libraries for api_version
from google.appengine.api import urlfetch
import json

#This initializes the jinja2 environment
#TEMPLATE CODE FOR APPS / boiler plate code
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#meme_templates = ["https://imgflip.com/s/meme/Distracted-Boyfriend.jpg", "https://imgflip.com/s/meme/Is-This-A-Pigeon.jpg", "https://imgflip.com/s/meme/Success-Kid.jpg", "https://i.imgflip.com/2/2kbn1e.jpg", "https://i.imgflip.com/2/22bdq6.jpg"]

#handler section
class HomePage(webapp2.RequestHandler):
    #request handler is the parent
    #gives us access that everything webapp has in its code

    def get(self): #request of getting stuff from a website
        home_dict {
        }
        welcome_template = jinja_env.get_template("main.html")
        self.response.write(welcome_template.render(home_dict)) #render takes in the jinja dict



class Vibe(webapp2.RequestHandler):
    def get(self):
        welcome_template = jinja_env.get_template("vibe.html")
        #self.response.write(welcome_template.render())
#
class ResultPage(webapp2.RequestHandler):
    def post(self):
        firstName = self.request.get("fname")
        lastName = self.request.get("lname")
        favColor = self.request.get("color") #if u only have this line, does not go back to page
        trueColor = self.request.get("TrueColor")
        favActivity = self.request.get("activity")
        music = self.request.get("music")
        user = Person(fName = fname, lName = lName, color= favColor, trueColor= trueColor, activity= favActivity, music=music)
        user.put()
        result_template = jinja_env.get_template("results.html")
        #self.response.write(result_template.render(data_dict))



app = webapp2.WSGIApplication(
    [
    ('/', HomePage),
    ('/result', ResultPage),
    ('/vibe', Vibe)
    ], debug = True

    #when you load up your application, and it ends w slash, this class should be handling all requests
    #reason it is an array is bc u can add others too
)
