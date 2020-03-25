# This gets data from Google Tag Manager api and returns a dataFrame

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os, sys, logging, json
import report
import auth

try:
    key_file = auth.auth("cj_data")
    SCOPES = ['https://www.googleapis.com/auth/tagmanager.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_file, SCOPES)
    tag_manager =  build('tagmanager', 'v2', credentials=credentials)

    mouseflow = "accounts/1090055821/containers/6311504/workspaces/1000189/variables/74"
    frame = pd.DataFrame()
except:
    print("An exception occurred importing gtm.py")


variable = tag_manager.accounts().containers().workspaces().variables().get(
    path=mouseflow
    ).execute()

para_list = variable["parameter"]
x = next(item for item in para_list if item["key"] == "map")
y = x["list"]


for item in y:
    url = item["map"][0]["value"]
    value = item["map"][1]["value"]

    row = {
    "url": url,
    "value": value
    }

    frame = frame.append(row,ignore_index = True)


return frame
