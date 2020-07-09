# This gets data from Google Analytics api and returns a dataFrame

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os, sys, logging
import report
import auth

try:
    key_file = auth.auth('cj_data')
    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_file, SCOPES)
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

except:
  print('An exception occurred importing ga_data.py')


def get_ga_report(**kwargs):
    view = kwargs['site']
    reporttype = kwargs['type']
    logger = logging.getLogger(__name__)
    period = kwargs['period']

    VIEW_ID_DICT = {
    'advisernet':os.environ.get('advisernet_ga'),
    'all':os.environ.get('all_ga'),
    'public':os.environ.get('public_ga')
    }

    VIEW_ID = VIEW_ID_DICT[view]

    rating_body = {
        'reportRequests': [{
            'viewId': VIEW_ID,
            'dateRanges': [{'startDate': '90daysAgo', 'endDate': 'yesterday'}],
            'metrics': [{'expression': 'ga:totalEvents'}],
            'dimensions': [
                {'name': 'ga:eventLabel'},
                {'name': 'ga:pagePath'},
                {'name': 'ga:dimension6'}],
            'filtersExpression': ('ga:dimension2!~Start|index;'
            'ga:pagePath!~/about-us/|/local/|/resources-and-tools/|\?;'
            'ga:eventCategory=~pageRating'),
            'orderBys': [{'fieldName': 'ga:totalEvents', 'sortOrder': 'DESCENDING'}],
            'pageSize': 10000
        }]
    }

    size_body = {
        'reportRequests': [{
            'viewId': VIEW_ID,
            'dateRanges': [{'startDate': '90daysAgo', 'endDate': 'yesterday'}],
            'metrics': [{'expression': 'ga:pageviews'}],
            'dimensions': [
                {'name': 'ga:pagePath'},
                {'name': 'ga:dimension6'}],
            'filtersExpression': ('ga:dimension2!~Start|index;'
            'ga:pagePath!~/about-us/|/local/|/resources-and-tools/|\?'),
            'orderBys': [{'fieldName': 'ga:pageviews', 'sortOrder': 'DESCENDING'}],
            'pageSize': 10000
            }]
    }

    REPORT_TYPE = {
        'rating':rating_body,
        'size':size_body
    }

    cols_dict = {
        'rating': {'ga:totalEvents':'totalEvents', 'ga:dimension6':'dimension6', 'ga:pagePath':'pagePath', 'ga:eventLabel':'eventLabel'},
        'size': {'ga:pageviews':'pageviews', 'ga:dimension6':'dimension6', 'ga:pagePath':'pagePath'}
    }

    report_body = REPORT_TYPE[reporttype]



    response =  analytics.reports().batchGet(
        body= report_body
        ).execute()

    

    cols = cols_dict[reporttype]
    df = pandafy(response)
    df2 = df.rename(index=str, columns=cols)

    return df2

########################################


def pandafy(response):
  list = []
  # get report data
  for report in response.get('reports', []):
    # set column headers
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])

    for row in rows:
        # create dict for each row
        dict = {}
        dimensions = row.get('dimensions', [])
        dateRangeValues = row.get('metrics', [])

        # fill dict with dimension header (key) and dimension value (value)
        for header, dimension in zip(dimensionHeaders, dimensions):
          dict[header] = dimension

        # fill dict with metric header (key) and metric value (value)
        for i, values in enumerate(dateRangeValues):
          for metric, value in zip(metricHeaders, values.get('values')):
            #set int as int, float a float
            if ',' in value or '.' in value:
              dict[metric.get('name')] = float(value)
            else:
              dict[metric.get('name')] = int(value)

        list.append(dict)

    df = pd.DataFrame(list)
    return df


# Run the functions in order
if __name__ == '__main__':
    pass