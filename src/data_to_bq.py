import os,sys
import report
from google.cloud import bigquery

gcp_project = os.environ.get('gcp_project')
bq_dataset = os.environ.get('bq_dataset') 
parentPath = report.parentPath


def send_data_bq(frame, name):

    length = frame.shape[0]
    table_id = ".".join([gcp_project,bq_dataset,name])

    client = bigquery.Client()

    strCols = frame.select_dtypes(include = ['object'])
    frame[strCols.columns] = strCols.apply(lambda x: x.str.replace('\n|\r', ' '))
    frame[strCols.columns] = strCols.apply(lambda x: x.astype('str'))

    job = client.load_table_from_dataframe(
        frame, table_id)

    job.result()

if __name__ == '__main__':
    name = sys.argv[1]
    send_data(data, name)