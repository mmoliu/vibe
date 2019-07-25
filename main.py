#main.py
import webapp2  #gives access to Google's deployment code
import jinja2
import os
from google.appengine.api import users
from models import Person, Message
from google.appengine.ext import ndb
import operator
import google.appengine.ext.db 
#libraries for api_version
from google.appengine.api import urlfetch
import json

MESSAGE_PARENT = ndb.Key("Entity", "strong_consistency")




#This initializes the jinja2 environment
#TEMPLATE CODE FOR APPS / boiler plate code
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# functions!!
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
        similarityIndex[str(person.first_name) + " " + str(person.last_name)] = percentMatch(user, person)
    sortedSimIndex = sorted(similarityIndex.items(), key=operator.itemgetter(1), reverse=True)
    return sortedSimIndex #returns a dictionary with the keys sorted by its value



#handler section
class HomePage(webapp2.RequestHandler):
    #request handler is the parent
    #gives us access that everything webapp has in its code

    def get(self): #request of getting stuff from a website

        #part of the copied bit
        user = users.get_current_user() # will return a user if someone is signed in, if not, none
        if user:
            email_address = user.nickname()
            self.response.write("You are logged in!")
            logout_url = users.create_logout_url('/')
            logout_button = "<a href='%s> Log out </a>" % logout_url

            existing_user = Person.query().filter(Person.email == email_address).get() #query if we already have that email #get pulls only one
            if existing_user:
                pass
            #self.response.write("You are logged in " + email_address +"!")
        else:
            self.response.write("You are a new user, please provide info!")
            login_url = users.create_login_url('/')
            login_button = "<a href='%s'> Sign In </a>" % login_url
            self.response.write("Please log in! <br>" + login_button)

        def post(self):
            user = users.get_current_user()
            if user:
                current_user = Person(
                    first_name=self.request.get('first_name'),
                    email = self.request.get("email_address"),

                )
                current_user.put()
                self.response.write("Thank you for registering!")
        home_dict={
        }
        welcome_template = jinja_env.get_template("html/main.html")
        self.response.write(welcome_template.render(home_dict)) #render takes in the jinja dict


class Vibe(webapp2.RequestHandler):
    def get(self):
        redirect= ""
        user = users.get_current_user() # will return a user if someone is signed in, if not, none
        if user:
            email_address = user.nickname()

            current_user = Person.query().filter(Person.email == email_address).get() #query if we already have that email #get pulls only one
            if current_user:
                pass
            self.response.write("You are logged in " + email_address +"!")
        else:
            redirect = '<meta http-equiv="Refresh" content="0.5; url=/register">'

        meta_data ={
         "redirect": redirect,
        }

        # if not existing_user or not user:
        #     self.response.write("<meta http-equiv="Refresh" content="0.5; url=/register" />")

        vibe_template = jinja_env.get_template("/html/vibe.html")
        self.response.write(vibe_template.render(meta_data))


class ResultPage(webapp2.RequestHandler):
    #an initialization of the creator's personalities #COME BACK TO THIS
    def post(self):
        firstName = self.request.get("fname")
        lastName = self.request.get("lname")
        favColor = self.request.get("color") #if u only have this line, does not go back to page
        trueColor = self.request.get("TrueColor")
        favActivity = self.request.get("activity")
        music = self.request.get("music")
        user = users.get_current_user()
        email_address = user.nickname()
        if user:
            current_user = Person.query().filter(Person.email == email_address).get()
            print(current_user)
            current_user.first_name = firstName
            current_user.last_name = lastName
            current_user.color = favColor
            current_user.trueColor= trueColor
            current_user.activity= favActivity
            current_user.music=music
            vibesList= getVibes(current_user) #list of tuples in order that have ppl's name, and similarity index
            print(vibesList)
            current_user.put()
        # else:
        #         noacc_user = Person(first_name = firstName, last_name = lastName, color= favColor, trueColor= trueColor, activity= favActivity, music=music)
        #         vibesList= getVibes(noacc_user) #list of tuples in order that have ppl's name, and similarity index
        #         noacc_user.put()

        data_dict = {
            "top_one": vibesList[1][0],
            #"lenVibes": len(vibesList[0][1]),
            "vibesList": vibesList,
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


class DiscussionPage(webapp2.RequestHandler):
    global MESSAGE_PARENT
    def get(self):
        result_template = jinja_env.get_template("/html/messaging.html")
        self.response.write(result_template.render())
    def post(self):
        user = users.get_current_user() # will return a user if someone is signed in, if not, none
        if user:
            email_address = user.nickname()
            name = Person.query().filter(Person.email == email_address).get()
            name = name.first_name
        content=self.request.get("text")
        msg = Message(parent=MESSAGE_PARENT, text = content)
        msg.put()
        #message_query = Message.query(kind=).fetch() #this is a list
        message_query = Message.query(ancestor=MESSAGE_PARENT).order(-Message.created).fetch() #Message.fetch()
        print(message_query)
        #need to get the key of a specific one, or make it ordered?
        message = []
        for i in message_query:
            message.append(i.text)
        print(message)
        text_dict = {
            "messages": message,
            "name": name
        }


        # query = client.query(kind='Task')
        # query.order = ['-created']
        result_template = jinja_env.get_template("/html/messaging.html")
        self.response.write(result_template.render(text_dict))



class Register(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user() # will return a user if someone is signed in, if not, none
        if user:
            email_address = user.nickname()
            existing_user = Person.query().filter(Person.email == email_address).get() #query if we already have that email #get pulls only one
            if not existing_user:
                email_address = user.nickname()
                current_user = Person(
                    first_name="something",
                    email = email_address,
                    last_name="None",
                    color="None",
                    trueColor="None",
                    activity="None",
                    music = "None",

                )
                current_user.put()
                self.response.write("Thank you for registering!")

            self.response.write("You are logged in! ")
            logout_url = users.create_logout_url('/register')
            logout_button = "<a href='%s'> Log out </a>" % logout_url
            self.response.write("Log out here: <br>"+ logout_button)
            #self.response.write("You are logged in " + email_address +"!")
        else:
            self.response.write("You are a new user, please provide info! ")
            login_url = users.create_login_url('/register')
            login_button = "<a href='%s'> Sign In </a>" % login_url
            self.response.write("Please log in! <br>" + login_button)

        reg_dict ={
        }
        register_template = jinja_env.get_template("/html/register.html")
        self.response.write(register_template.render(reg_dict))



#initialization
app = webapp2.WSGIApplication(
    [
    ('/', HomePage),
    ('/result', ResultPage),
    ('/vibe', Vibe),
    ('/video', Video),
    ('/register', Register),
    ('/messaging', DiscussionPage)
    ], debug = True

    #when you load up your application, and it ends w slash, this class should be handling all requests
    #reason it is an array is bc u can add others too
)
