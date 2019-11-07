import os
from dotenv import load_dotenv

path1 = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(path1)
load_dotenv(os.path.join(parentPath, '.env'))


from epi_report import epi_pages_report
from data_to_bq import send_data_bq
from ga_data import get_ga_report


sources = {
    "epi": epi_pages_report,
    "ga":get_ga_report
}
class report:
    def __init__(self, name=None, data=None, source=None, site=None, source_args=None, dest=None, status=None):
        self.name = name
        self.data = data
        self.source = source
        self.site = site
        self.source_args = source_args
        self.dest = dest
        self.status = status
        self.source_fn = sources[self.source]

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
            send_data_bq(self.data, self.name)
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




print ("hello Ian")
