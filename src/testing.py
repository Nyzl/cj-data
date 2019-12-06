from google.cloud import storage
from pathlib import Path
import os,json


path1 = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(path1)

def test2():

    path1 = os.path.dirname(os.path.realpath(__file__))
    parentPath = os.path.dirname(path1)
    destination_file_name = os.path.join(parentPath,"store","test.json")

    bucket_name = "customerjourney_service"
    source_blob_name= "epi.json"


    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    x = blob.download_as_string().decode('utf8')

    y = json.loads(x)

    print(y['user_name'])

    return str(x)

if __name__ == '__main__':
    test2()