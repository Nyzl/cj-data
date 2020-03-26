# This gets data from Google Search Console api and returns a dataFrame

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os, sys, logging
import report
import auth


def get_search(*args,**kwargs):
    key_file = auth.auth("cj_data")
    SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_file, SCOPES)
    search_console =  build('webmasters', 'v3', credentials=credentials)
    property_uri = 'https://www.citizensadvice.org.uk/'

    # test request to get a list of sites
    site_list = search_console.sites().list().execute()


    request = {
        "startDate": "2020-01-01",
        "endDate": "2020-03-31",
        "dimensions": ["query"],
        "searchType": "web",
        "dimensionFilterGroups": [
            {
                "groupType": "and",
                "filters": [
                    {
                        "dimension": "page",
                        "expression": "coronavirus",
                        "operator": "contains"
                    }
                ]
            }
        ],
        'rowLimit': 25000,
        'startRow': 0
    }

   
    response = search_console.searchanalytics().query(siteUrl=property_uri, body=request).execute()
    rows = response['rows']
    frame = pd.DataFrame(rows)
    frame['query'] = [' '.join(map(str, l)) for l in frame['keys']]

    return frame







if __name__ == '__main__':
    get_search()