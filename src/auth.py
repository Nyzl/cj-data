# This goes to a google cloud storage bucket and gets a json file

import json
#from google.cloud import storage

def auth(name):
    bucket_name = 'customerjourney_service'
    source_blob_name= name+'.json'
    #storage_client = storage.Client()
    #bucket = storage_client.get_bucket(bucket_name)
    #blob = bucket.blob(source_blob_name)
    #blob_string = blob.download_as_string().decode('utf8')
    #auth_json = json.loads(blob_string)

    return bucket_name

if __name__ == '__main__':
    pass