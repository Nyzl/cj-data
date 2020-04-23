# This gets data from Google Search Console api and returns a dataFrame

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import os, sys, logging, string
import report
import auth
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

def get_data(**kwargs):
    key_file = auth.auth('cj_data')
    SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_file, SCOPES)
    search_console =  build('webmasters', 'v3', credentials=credentials)
    property_uri = 'https://www.citizensadvice.org.uk/'

    # test request to get a list of sites
    site_list = search_console.sites().list().execute()

    # dates are in the format YYYY-MM-DD

    startDate = kwargs['startDate']
    endDate = kwargs['endDate']
    startRow = kwargs['startRow']


    request = {
        'startDate': startDate,
        'endDate': endDate,
        'dimensions': ['query', 'device', 'page', 'date'],
        'searchType': 'web',
        'rowLimit': 25000,
        'startRow': startRow
    }

   
    response = search_console.searchanalytics().query(siteUrl=property_uri, body=request).execute()
    if len(response) > 1:
        rows = response['rows']

        df = pd.DataFrame.from_dict(rows)
        df[['query','device', 'page', 'date']] = pd.DataFrame(df['keys'].values.tolist(), index= df.index)
        result = df.drop(['keys'],axis=1)
        

        return result
    else:
        pass

    


def clean(frame): 
    frame['query'] = frame['query'].apply(lambda x: x.lower())
    frame['query'] = frame['query'].apply(lambda x: x.translate(string.punctuation))
    frame['query'] = frame['query'].apply(lambda x: x.translate(string.digits))
    frame['tokens'] = frame['query'].apply(lambda x: x.split(" "))
    frame = frame.explode('tokens')

    stop = set(stopwords.words('english'))
    stop.add('uk')
    frame = frame[~frame['tokens'].isin(stop)]

    lemma = WordNetLemmatizer()
    frame['tokens'] = frame['tokens'].apply(lambda x: lemma.lemmatize(x, pos="v"))
    

    return frame




if __name__ == '__main__':
    pass