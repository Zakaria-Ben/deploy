import sys
import requests
import json
from pathlib import Path

# single request for pulling lax paring lots information from web API and sending it to a mediator endpoint

url_laxparking='https://data.lacity.org/resource/xzkr-5anj.json'
url_mediator='http://127.0.0.1:1112'

# Call laxparking and retrieve array for lot availability
json_array=requests.get(url_laxparking,verify=False).json()   #Gets data from SODA API

# loop over all lots and send post API request to laxparking mediator's endpoint
for json_data in json_array:
    print(json_data)
    try:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url_mediator, data=json.dumps(json_data), headers=headers)
        print(response.status_code)
    except Exception as inst:
        print('exception when calling mediator endpoint')
