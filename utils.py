import sys
sys.path.insert(0, 'libs')
from google.appengine.api import app_identity, mail, urlfetch
import cloudstorage
import datetime


def save_to_bucket(file_name, content, mode='r'):
    bucket_name = app_identity.get_default_gcs_bucket_name()
    return_string = ''
    try:
        full_name = '/' + bucket_name + '/' + file_name
        # Append is not supported by Google Cloud Storage
        if mode == 'a':
            f = cloudstorage.open(full_name, 'r')
            old_data = f.read()
            new_data = old_data + '\n' + content
            f.close()
            f = cloudstorage.open(full_name, 'w')
            f.write(new_data)
            f.close()
            return_string += 'OK: ' + file_name + ' appended to bucket<br>'
        elif mode == 'w':
            f = cloudstorage.open(full_name, 'w')
            f.write(content)
            f.close()
            return_string += 'OK: ' + file_name + ' rewrote to bucket<br>'
        else:
            return_string += 'Error: Saving mode \'' + mode + '\' unknown for ' + file_name + '<br>'
    except:
        return_string += 'Error: Saving crashed for ' + file_name + '<br>'
    return return_string

def get_from_bucket(file_name):
    bucket_name = app_identity.get_default_gcs_bucket_name()
    return_string = ''
    try:
        full_name = '/' + bucket_name + '/' + file_name
        # Append is not supported by Google Cloud Storage
        f = cloudstorage.open(full_name, 'r')
        return_string = f.read()
        f.close()
    except:
        return_string += 'Error: Impossible to get the data for  ' + file_name + '<br>'
    return return_string

def send_email(subject='Error', body='Envoye depuis GAE'):
    try:
        message = mail.EmailMessage(sender='Bot RateSetter <bot@rate-setters.appspotmail.com>', subject=subject)
        message.to = 'Alfred Bourely <alfred.bourely@hotmail.fr>'
        message.body = body
        message.send()
        return_string = 'OK: Email sent to Alfred<br>'
    except:
        return_string = 'Error: email not sent to Alfred'
        current_time = str(datetime.datetime.now())[:19]
        log = current_time + ', ' + return_string
        log += ', Subject: ' + subject + ', Body: ' + body
        save_to_bucket('errors.csv', log, mode='a')
    return return_string

def get_html(url):
    result = urlfetch.fetch(url, headers = {'Cache-Control' : 'max-age=30'})
    if result.status_code == 200:
        return_string = 'Download finished for : ' + url + '<br>'
        return return_string, result.content
    else:
        return_string = 'Error in downloading : ' + url + '<br>'
        current_time = str(datetime.datetime.now())[:19]
        log = current_time + ', ' + return_string
        save_to_bucket('errors.csv', log, mode='a')
        subject = 'Connection failed'
        body = 'Impossible de se connecter'
        send_email(subject, body)
        return return_string, ''












