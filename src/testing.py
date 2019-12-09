import pandas as pd
from google.cloud import bigquery

raw_data = {'first_name': ['Stevil', 'Molly', 'Tina', 'Jake', 'Amy'], 
        'last_name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze'], 
        'age': [42, 52, 36, 24, 73], 
        'preTestScore': [4, 24, 31, 2, 3],
        'postTestScore': [25, 94, 57, 62, 70]}
frame = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])


def test2(frame):
    client = bigquery.Client()
    table_id = "customerjourney-214813.IanTest.testytest"

    strCols = frame.select_dtypes(include = ['object'])
    frame[strCols.columns] = strCols.apply(lambda x: x.str.replace('\n|\r', ' '))
    frame[strCols.columns] = strCols.apply(lambda x: x.astype('str'))

    job = client.load_table_from_dataframe(
        frame, table_id)

    job.result()






if __name__ == '__main__':
    pass