# This gets data from the Trello api

import pandas as pd
import requests,json
import auth

auth_json = auth.auth('trello')
key = auth_json['key']
token = auth_json['token']

data_science_board = '591eea14bb540d56a3948f7f'
Done2019 = '591eee752f6a8bbe9687acff'

'''
/lists/{id}/cards
'''

url = 'https://api.trello.com/1/lists/' + lst + '/cards?pluginData=true'
payload = {'key': key, 'token': token, 'fields': ['name','labels', 'idList', 'url', 'due']}
response = requests.get(url, params = payload)
return response.json()