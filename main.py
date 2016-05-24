import webapp2
from provision import Provision
from datadump import Datadump

class MainHandler(webapp2.RequestHandler):
    def get(self):
        provision = Provision()
        html = provision.run()
        datadump = Datadump()
        html += datadump.run()
        self.response.write(html)

app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
