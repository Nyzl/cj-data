# This gets a csv report from episerver and returns a dataFrame

import pandas as pd
import csv,requests,os,sys,json
from io import StringIO
from datetime import datetime
from .auth import auth

auth_json = auth('epi')
username = auth_json['user_name']
password = auth_json['password']
details = 'username=' + username + '&password=' + password
edit_login = auth_json['auth_uri'] + details

public = auth_json['public_report']
advisernet = auth_json['advisernet_report']

feedback30 = 'placeholder'
feedback60 = 'placeholder'

urls = {
    'public' : public,
    'advisernet': advisernet,
    'feedback30': feedback30,
    'feedback60': feedback60
}

#def epi_report(site, *args, **kwargs): 
def epi_report(**kwargs):
    site = kwargs['site']    
    url = urls[site]    
    auth_json = auth.auth('epi')
    username = auth_json['user_name']
    password = auth_json['password']
    details = 'username=' + username + '&password=' + password
    edit_login = auth_json['auth_uri'] + details

    with requests.Session() as login:
        login.get(edit_login)
        # wrapping next line in a 'with' statement to hopefully reduce failures
        # makes requests release the connection properly when stream = True
        with login.get(url, stream = True) as getting:
            sheet = StringIO(getting.text)

        frame = pd.read_csv(sheet)

        return frame


def pages_clean(frame):
    site = 'https://www.citizensadvice.org.uk'
    country_code = dict([
        ('en-GB',''),
        ('en-SCT','/scotland'),
        ('en-NIR','/nireland'),
        ('en-WLS','/wales'),
        ('cy','/cymraeg')
    ])  

    frame['url'] = frame['Language']
    frame['url'] = frame['url'].replace(country_code)
    frame['url'] = site+frame['url']+frame['Path']
    
    #frame.loc[frame['LastAccuracyReview'] == '01/01/0001 00:00:00','LastAccuracyReview'] = None
    # errors = 'coerce', dayfirst = True, format = '%d/%m/%Y'
    frame['LastAccuracyReview'] = pd.to_datetime(frame['LastAccuracyReview'], errors = 'coerce')
    
    #frame.loc[frame['ReviewDate'] == '01/01/0001 00:00:00','ReviewDate'] = None
    frame['ReviewDate'] = pd.to_datetime(frame['ReviewDate'], errors = 'coerce')

    frame['StopPublish'] = pd.to_datetime(frame['StopPublish'], errors = 'coerce')
    frame['StartPublish'] = pd.to_datetime(frame['StartPublish'], errors = 'coerce')
    frame['Changed'] = pd.to_datetime(frame['Changed'], errors = 'coerce')
    
    

    return frame 


if __name__ == '__main__':
    pass