# This gets data from Google Search Console api and returns a dataFrame

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import os, sys, logging, string
import report
import auth

#from textblob import TextBlob
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

pd.options.display.max_colwidth = 1000

def get_data(*args,**kwargs):
    key_file = auth.auth("cj_data")
    SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_file, SCOPES)
    search_console =  build('webmasters', 'v3', credentials=credentials)
    property_uri = 'https://www.citizensadvice.org.uk/'

    # test request to get a list of sites
    site_list = search_console.sites().list().execute()


    request = {
        "startDate": "2020-01-01",
        "endDate": "2020-01-01",
        "dimensions": ["query", "device", "page", "date"],
        "searchType": "web",
        'rowLimit': 25000,
        'startRow': 0
    }

   
    response = search_console.searchanalytics().query(siteUrl=property_uri, body=request).execute()
    rows = response['rows']

    df = pd.DataFrame.from_dict(rows)
    new_cols = df['keys'].astype(str).str.replace("[","").str.replace("]","")
    new_cols = new_cols.str.split(pat=',',expand=True,n=3)
    new_cols.columns = ["query", "device", "page", "date"]
    new_cols['device'] = new_cols['device'].str.replace("'","").str.lower()
    new_cols['query'] = new_cols['query'].str.replace("'","")
    new_cols['page'] = new_cols['page'].str.replace("'","")
    new_cols['date'] = new_cols['date'].str.replace("'","")
    new_cols['key'] = df['keys']
    result = pd.concat([new_cols,df], axis=1, join='inner')
    result = result.drop(["key","keys"],axis=1)

    frame = clean(result)
    
    return frame


def clean(frame): 
    frame['query'] = frame['query'].apply(lambda x: x.lower())
    frame['query'] = frame['query'].apply(lambda x: x.translate(string.punctuation))
    frame['query'] = frame['query'].apply(lambda x: x.translate(string.digits))
    frame['tokens'] = frame['query'].apply(lambda x: x.split(" "))
    frame = frame.explode('tokens')

    stop = set(stopwords.words('english'))
    stop.add("uk")
    frame = frame[~frame['tokens'].isin(stop)]

    lemma = WordNetLemmatizer()
    frame['tokens'] = frame['tokens'].apply(lambda x: lemma.lemmatize(x, pos="v"))
    

    return frame


if __name__ == '__main__':
    frame = get_data()
    print(frame.shape)