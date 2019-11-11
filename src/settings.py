import os, dotenv

path1 = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(path1)
dotenv.load_dotenv(os.path.join(parentPath, '.env'))

import data_to_bq

class report:
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
            self.status = err
        
        print(self.status)
        return "all done"
        
    
    def send_data(self):
        try:
            data_to_bq.send_data_bq(self.data, self.name)
            self.status = "sent"
        except Exception as err:
            self.status = err

        print(self.status)
        return "sent all the data"

    def clean_data(self):
        x = "when i'm cleaning data"

        #strCols = frame.select_dtypes(include = ['object'])
        #frame[strCols.columns] = strCols.apply(lambda x: x.str.replace('\n|\r', ' '))
        #frame[strCols.columns] = strCols.apply(lambda x: x.astype('str'))

    def save_data(self):
        if self.status == 'got':
            print("i'm going to save this data")
        else:
            print("i'm not sure i got the data")





print ("hello Ian")
