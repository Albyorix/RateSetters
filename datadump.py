from utils import *
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app


class Datadump:

    def __init__(self):
        self.write = ''

    def run(self):
        datadump_url = 'https://www.ratesetter.com/lend/datadump'
        datadump_csv = 'datadump.csv'
        result_string, datadump_html = get_html(datadump_url)
        self.write += result_string
        output = save_to_bucket(datadump_csv, datadump_html, 'w')
        if output[:5] == 'Error':
            subject = 'Saving ' + datadump_csv + ' failed'
            send_email(subject, body=output)
        self.write += output
        return self.write

class MainHandler(webapp2.RequestHandler):
    def get(self):
        datadump = Datadump()
        html = datadump.run()
        self.response.write(html)

app = webapp2.WSGIApplication([('/datadump', MainHandler)], debug=True)

if __name__ == '__main__':
    run_wsgi_app(app)







