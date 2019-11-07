import requests
import pandas as pd
import os
from io import StringIO
import sys
import time
from pathlib import Path
from google.oauth2 import service_account
import pandas_gbq
import settings

gcp_project = os.environ.get('gcp_project')
bq_dataset = os.environ.get('bq_dataset') 
parentPath = settings.parentPath


# get file, upload file, delete file
def send_data_bq(data, name):
    
    #file = os.path.join(parentPath,"store",name + ".pkl")

    frame = data
    length = frame.shape[0]

    KEY_FILE_LOCATION = os.path.join(parentPath,"creds","datapipeline.json")
    credentials = service_account.Credentials.from_service_account_file(KEY_FILE_LOCATION)

    strCols = frame.select_dtypes(include = ['object'])
    frame[strCols.columns] = strCols.apply(lambda x: x.astype('str'))

    i = 0
    j = 5000

    while i < length:
        out = frame.iloc[i:j]
        out.to_gbq(bq_dataset+name, gcp_project,
                   if_exists = 'append', private_key=KEY_FILE_LOCATION)

        time.sleep(60)

        i = j
        j = j+5000

    #os.remove(file)

    return 1


    #frame will need cleaning
if __name__ == '__main__':
    name = sys.argv[1]
    send_data(data, name)