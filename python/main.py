#main.py
import webapp2  #gives access to Google's deployment code
import jinja2
import os
from models import MemeInfo

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
class MainPage(webapp2.RequestHandler):
    #request handler is the parent
    #gives us access that everything webapp has in its code
    def get(self): #request of getting stuff from a website
        # self.response.headers['Content-Type'] = 'text/html' #expect text
        # self.response.write("<h1>The Art of Mochi </h1>")
        api_url = "https://api.imgflip.com/get_memes"
        api_url2 ="https://api.imgflip.com/caption_image"
        imgflip_response = urlfetch.fetch(api_url).content #fetches the api_url and the stuff that's there
        imgflip_caption = urlfetch.fetch(api_url2).content

        imgflip_response_json= json.loads(imgflip_response)
        meme_template = []
        for meme in imgflip_response_json["data"]["memes"]:
            meme_template.append(meme["url"])
        meme_dict = {
            "imgs": meme_template
        }
        welcome_template = jinja_env.get_template("welcome.html")
        self.response.write(welcome_template.render(meme_dict)) #render takes in the jinja dict



class AllMemesPage(webapp2.RequestHandler):
    def get(self):
        allmemes= {
        "memelist": MemeInfo.query().fetch(),

        }
        welcome_template = jinja_env.get_template("allmemes.html")
        self.response.write(welcome_template.render(allmemes))
#
class ResultPage(webapp2.RequestHandler):
    def post(self):
        top_line = self.request.get("top-line") #if u only have this line, does not go back to page
        bot_line = self.request.get("bot-line")
        meme_url = self.request.get("template")
        meme1 = MemeInfo(memeline1 = top_line, memeline2= bot_line, img =meme_url)

        meme1.put()

        data_dict={
            "top_line": top_line,
            "bot_line": bot_line,
            "meme_url": meme_url

        }
        result_template = jinja_env.get_template("result.html")
        self.response.write(result_template.render(data_dict))



app = webapp2.WSGIApplication(
    [
    ('/', MainPage),
    ('/result', ResultPage),
    ('/allmemes', AllMemesPage)
    ], debug = True

    #when you load up your application, and it ends w slash, this class should be handling all requests
    #reason it is an array is bc u can add others too
)
