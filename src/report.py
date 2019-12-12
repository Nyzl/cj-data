import sys,os,dotenv
import pandas as pd
import pickle

path1 = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(path1)
dotenv.load_dotenv(os.path.join(parentPath, '.env'))

import data_to_bq

class Report:
    def __init__(self, name=None, data=None, source=None, site=None, source_args=None, dest=None, status=None, source_fn=None):
        self.name = name
        self.data = data
        self.source = source
        self.site = site
        self.source_args = source_args
        self.dest = dest
        self.status = status
        self.source_fn = source_fn

    def get_data(self):
        try:
            self.data = self.source_fn(self.site, self.source_args)
            self.status = "got"
        except Exception as err:
            self.status = str(err)
            print(self.status)
        
    
    def send_data(self):
        try:
            data_to_bq.send_data_bq(self.data, self.name)
            self.status = "sent"
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


