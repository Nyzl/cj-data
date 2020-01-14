import sys,os,dotenv
import pandas as pd
import pickle
from datetime import date
import data_to_bq
from google.cloud import bigquery

gcp_project = os.environ.get('gcp_project')
bq_dataset = os.environ.get('bq_dataset')

class Report:
    def __init__(self, name=None, source=None, site=None, source_args=None, dest=None, source_fn=None, status="Initialised", date=date.today()):
        self.name = name
        self.data = pd.DataFrame()
        self.source = source
        self.site = site
        self.source_args = source_args
        self.dest = dest
        self.status = status
        self.source_fn = source_fn
        self.date = date

    def get_data(self):
        try:
            self.data = self.source_fn(self.site, self.source_args)
            self.status = "got"
            self.date = date.today()
        except Exception as err:
            self.status = str(err)
            print(self.status)
        
    
    def send_data(self):
        print("sending data to bq")
        try:
            data_to_bq.send_data_bq(self.data, self.name)
            self.status = "sent"
            self.date = date.today()
        except Exception as err:
            self.status = str(err)
            print(self.status)


    def clean_data(self):
        frame = pd.DataFrame(self.data)
        strCols = frame.select_dtypes(include = ['object'])
        frame[strCols.columns] = strCols.apply(lambda x: x.str.replace('\n|\r', ' '))

        self.data = frame


    def save_data(self):
        if self.status == 'got':
            with open(parentPath+"/store/"+self.name+".pkl", 'wb') as file:
                pickle.dump(self, file)
        else:
            print("i'm not sure i got the data")

    def get_upload_date(self):
        table_id = ".".join([gcp_project,bq_dataset,self.name])
        client = bigquery.Client()

        table = client.get_table(table_id)
        self.date = table.modified


