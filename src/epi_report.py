import pandas as pd
import csv,requests,os,sys,json
from io import StringIO
from datetime import datetime
import auth

auth_json = auth.auth("epi")
username = auth_json['user_name']
password = auth_json['password']
details = "username=" + username + "&password=" + password
edit_login = auth_json['auth_uri'] + details

public = auth_json['public_report']
advisernet = auth_json['advisernet_report']

feedback30 = "placeholder"
feedback60 = "placeholder"

def epi_pages_report(site, *args):    
    urls = {
        "public" : public,
        "advisernet" : advisernet
    }

    url = urls[site]    
    frame = makeFrame(url)
    return frame

#def epi_report(site, *args):



def makeFrame(link):
    auth_json = auth.auth("epi")
    username = auth_json['user_name']
    password = auth_json['password']
    details = "username=" + username + "&password=" + password
    edit_login = auth_json['auth_uri'] + details

    now = datetime.now()
    today = datetime.date(now)
    site = 'https://www.citizensadvice.org.uk'
    country_code = dict([
        ('en-GB',''),
        ('en-SCT','/scotland'),
        ('en-NIR','/nireland'),
        ('en-WLS','/wales'),
        ('cy','/cymraeg')
    ])
    with requests.Session() as login:
        login.get(edit_login)
        # wrapping next line in a 'with' statement to hopefully reduce failures
        # makes requests release the connection properly when stream = True
        with login.get(link, stream = True) as getting:
            sheet = StringIO(getting.text)

        frame = pd.read_csv(sheet)

        frame['ReportDate'] = today
        frame['url'] = frame['Language']
        frame['url'] = frame['url'].replace(country_code)
        frame['url'] = site+frame['url']+frame['Path']
        frame.loc[frame['LastAccuracyReview'] == '01/01/0001 00:00:00','LastAccuracyReview'] = None
        frame.loc[frame['ReviewDate'] == '01/01/0001 00:00:00','ReviewDate'] = None
        frame['ReportDate'] = pd.to_datetime(frame['ReportDate'], errors = 'ignore', yearfirst = True)
        frame['StopPublish'] = pd.to_datetime(frame['StopPublish'], errors = 'ignore', dayfirst = True)
        frame['StartPublish'] = pd.to_datetime(frame['StartPublish'], errors = 'ignore', dayfirst = True)
        frame['Changed'] = pd.to_datetime(frame['Changed'], errors = 'ignore', dayfirst = True)
        frame['ReviewDate'] = pd.to_datetime(frame['ReviewDate'], errors = 'ignore', dayfirst = True)
        frame['LastAccuracyReview'] = pd.to_datetime(frame['LastAccuracyReview'], errors = 'ignore', dayfirst = True)
        strCols = frame.select_dtypes(include = ['object'])
        frame[strCols.columns] = strCols.apply(lambda x: x.str.replace('\n|\r', ' '))
        frame[strCols.columns] = strCols.apply(lambda x: x.astype('str'))

        return frame




if __name__ == '__main__':
    site = sys.argv[1]
    epi_pages_report(site)