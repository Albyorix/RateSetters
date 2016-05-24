from utils import *
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app


class Risk:

    def __init__(self):
        self.write = ''

    def run(self):
        provision_csv = 'provision.csv'
        output = get_from_bucket(provision_csv)
        if output[:5] == 'Error':
            subject = 'Risk management failed'
            send_email(subject, body=output)
            self.write += "Error, email sent"
        else:
            # Check if last day data has been downloaded
            self.check_data_dl(output)
            # Check if fall is more than 5%
            max_authorised_drawdown = 0.05
            self.check_current_dd(output, max_authorised_drawdown)
            if self.write != '':
                self.write += "There are no risk at this point"
        return self.write
        
    def check_data_dl(self, output):
        day = str(datetime.datetime.now())[:10]
        last_day = output.split('\n')[-1].split(',')[0][:10]
        if day != last_day:
            subject = 'Problem in date'
            send_email(subject, body=output.split('\n')[-1])
            self.write += "Error in date, email sent"

    def check_current_dd(self, output, max_auth_dd):
        output = output.split('\n')
        for i in range(1, len(output)):
            output[i] = output[i].split(', ')
        max1 = 0
        max2 = 0
        for i in range(1, len(output)):
            if int(output[i][1]) > max1:
                max1 = int(output[i][1])
            if int(output[i][2]) > max2:
                max2 = int(output[i][2])
        current1 = output[-1][1]
        current2 = output[-1][2]

        email_output = "current provision:" + str(current1)
        email_output += "\nmax provision:" + str(max1)
        email_output += "\ncurrent security:" + str(current2)
        email_output += "\n max security:" + str(max2)
        if current1 < max1*(1-max_auth_dd) or current2 < max2:
            subject = 'Risk on RateSetters'
            send_email(subject, body=email_output)
            self.write += "Error in date, email sent"

class MainHandler(webapp2.RequestHandler):
    def get(self):
        risk = Risk()
        html = risk.run()
        self.response.write(html)

app = webapp2.WSGIApplication([('/risk', MainHandler)], debug=True)

if __name__ == '__main__':
    run_wsgi_app(app)







