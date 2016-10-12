from utils import *
import webapp2
import datetime
from bs4 import BeautifulSoup
from google.appengine.ext.webapp.util import run_wsgi_app


class Provision:

    def __init__(self):
        self.write = ''

    def run(self):
        provision_url =  'https://www.ratesetter.com/invest/everyday-account/protection'
        provision_csv = 'provision.csv'
        result_string, provision_html = get_html(provision_url)
        line = self.find_content_from_provision(provision_html)
        output = save_to_bucket(provision_csv, line, 'a')
        if output[:5] == 'Error':
            subject = 'Saving ' + provision_csv + ' failed'
            send_email(subject, body=output)
        self.write += output
        return self.write

    def find_content_from_provision(self, provision_html):
        soup = BeautifulSoup(provision_html)
        security = int(soup.find('h2', 'hero-provision-amount').string[1:].replace(' million','000000'))
        provision = int(soup.find('span', 'value hidden-xs').contents[0][1:].replace(',',''))
        hour = str(datetime.datetime.now())[:19]
        line = hour + ', ' + str(provision) + ', ' + str(security)
        self.write += 'Data found in provision<br>'
        return line


class MainHandler(webapp2.RequestHandler):
    def get(self):
        provision = Provision()
        html = provision.run()
        self.response.write(html)

app = webapp2.WSGIApplication([('/provision', MainHandler)], debug=True)

if __name__ == '__main__':
    run_wsgi_app(app)







