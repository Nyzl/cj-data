# This defines the report object

import sys,os,dotenv
import pandas as pd
import pickle
from datetime import date
import data_to_bq
from google.cloud import bigquery

gcp_project = os.environ.get('gcp_project')
bq_dataset = os.environ.get('bq_dataset')

class Report:
    def __init__(self, name=None, source=None, site=None, source_args=None, source_fn=None, dest=None, source_args_test=None):
        self.name = name
        self.source = source
        self.site = site
        self.source_args = source_args
        self.source_fn = source_fn
        self.dest = dest
        self.date = date.today()
        self.status = "Initialised"
        self.data = pd.DataFrame()
        self.source_args_test = source_args_test

    def get_data(self):
        try:
            self.data = self.source_fn(self.site, self.source_args)
            self.data_test = self.source_fn(self.source_args_test)
            self.status = "got"
            self.date = date.today()
        except Exception as err:
            self.status = str(err)
            print(self.status)
            raise err
        
    
    def send_data(self):
        try:
            data_to_bq.send_data_bq(self.data, self.name)
            self.status = "sent"
            self.date = date.today()
        except Exception as err:
            self.status = str(err)
            print(self.status)
            raise err

    def clean_data(self):
        frame = self.data

        try:
            self.cleaning(frame)
        except AttributeError as err:
            pass

        strCols = frame.select_dtypes(include = ['object'])
        frame[strCols.columns] = strCols.apply(lambda x: x.str.replace('\n|\r', ' '))
        frame[strCols.columns] = strCols.apply(lambda x: x.astype('str')) 
        self.data = frame


    def get_upload_date(self):
        table_id = ".".join([gcp_project,bq_dataset,self.name])
        client = bigquery.Client()
        table = client.get_table(table_id)
        modified = table.modified
        self.date = modified
        self.strDate = modified.strftime("%d/%b/%Y, %H:%M:%S")



