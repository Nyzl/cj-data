# This sends a Pandas dataFrame to Big Query

import os
import pandas as pd
from google.cloud import bigquery

gcp_project = os.environ.get('gcp_project')
bq_dataset = os.environ.get('bq_dataset') 


def send_data_bq(frame, name):
    table_id = ".".join([gcp_project,bq_dataset,name])

    client = bigquery.Client()

    strCols = frame.select_dtypes(include = ['object'])
    frame[strCols.columns] = strCols.apply(lambda x: x.str.replace('\n|\r', ' '))

    schema = []
    strCols = frame.select_dtypes(include = ['object'])
    for s in strCols:
        schema.append(bigquery.SchemaField(s, bigquery.enums.SqlTypeNames.STRING))

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        # WRITE_TRUNCATE, WRITE_APPEND, WRITE_EMPTY
        write_disposition="WRITE_TRUNCATE",
    )

    job = client.load_table_from_dataframe(
        frame, 
        table_id, 
        num_retries=6, 
        location='EU', 
        job_config=job_config
    )

    job.result()

if __name__ == '__main__':
    pass