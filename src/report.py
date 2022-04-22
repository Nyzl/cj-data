# This defines the report object

import sys,os
import pandas as pd
import pickle
from datetime import date
#from .data_to_bq import send_data_bq
#from google.cloud import bigquery

send_data_bq = ''
gcp_project = os.environ.get('gcp_project')
bq_dataset = os.environ.get('bq_dataset')

class Report:
    def __init__(self, name=None, source=None, site=None, source_args=None, source_fn=None, clean_fn=None, dest=None, source_kwargs={}, send_kwargs={}, clean_kwargs={}):
        self.name = name
        self.source = source
        self.site = site
        self.source_args = source_args
        self.source_fn = source_fn
        self.clean_fn = clean_fn
        self.dest = dest
        self.date = date.today()
        self.status = 'Initialised'
        self.data = pd.DataFrame()
        self.source_kwargs = source_kwargs
        self.send_kwargs = send_kwargs
        self.clean_kwargs = clean_kwargs


    def get_data(self):
        try:
            #self.data = self.source_fn(self.site, self.source_args)
            self.data = self.source_fn(**self.source_kwargs)
            self.status = 'got'
            self.date = date.today()
        except Exception as err:
            self.status = str(err)
            print(self.status)
            raise err
        
    
    def send_data(self):
        try:
            send_data_bq(frame=self.data, name=self.name, **self.send_kwargs)
            self.status = 'sent'
            self.date = date.today()
        except Exception as err:
            self.status = str(err)
            print(self.status)
            raise err

    def clean_data(self):
        frame = self.data
        try:
            frame = self.clean_fn(frame=self.data, **self.clean_kwargs)
        except AttributeError as err:
            pass
        except TypeError as err:
            pass

        self.data['report_date'] = pd.to_datetime('today')
        self.data['report_date'] = self.data['report_date'].dt.date
        self.data['report_date'] = pd.to_datetime(self.data['report_date'])

        strCols = frame.select_dtypes(include = ['object'])
        frame[strCols.columns] = strCols.apply(lambda x: x.str.replace('\n|\r', ' '))
        frame[strCols.columns] = strCols.apply(lambda x: x.astype('str')) 
        self.data = frame


    def get_upload_date(self):
        try:
            table_id = ".".join([gcp_project,bq_dataset,self.name])
            #client = bigquery.Client()
            #table = client.get_table(table_id)
            #modified = table.modified
            modified = '01/01/2022'
            self.date = modified
            self.strDate = modified.strftime("%d/%b/%Y, %H:%M:%S")
        except Exception as err:
            self.strDate = str(err)
            #raise err



