import requests
import json
import pprint
from decouple import config

# import common code snippets / helpers from another folder
#   - or copy the ref 'from' files in this folder and from-import it directly 
#   - without the 'import sys,os' and 'sys.path..' lines.
import sys, os
sys.path.insert(1,os.path.join('..','..','lib'))
from get_yaml_from_excel import get_yaml_from_excel



#### Process AMP group creation responce
def amp_group_create_res(
    k,          # index
    v           # contents
    ):
    if k==0:
        print(f"API Rate Limit Remaining/Total/Seconds-to-reset: "+
              f"{resp.headers['X-RateLimit-Remaining']}/"+
              f"{resp.headers['X-RateLimit-Limit']}/"+
              f"{resp.headers['X-RateLimit-Reset']}",
              )
    
    if resp.status_code == 201:
        print(f"OK - {v['name']} created. GUID = {resp.json()['data']['guid']}")
    else:
        e = resp.json()["errors"][0]
        print(f"FAIL - {v['name']} failed to create."+
              f" API Result = {resp.status_code} {resp.reason}."+
              f" ERROR = {e['error_code']} - {e['description']} - {e['details'][0]}",
              )


#### Read YAML data from Excel worksheet
input_data = get_yaml_from_excel(
    wbn="group_create.xlsx",
    wsn="groups",
    col_yaml_name="_yaml",
    )


#### Create AMP Groups - REST API Calls
api_base_url = 'https://api.apjc.amp.cisco.com/v1/'
api_client_id = config('AMP_CLIENT_ID')
api_api_key = config('AMP_API_KEY')
api_path = "groups"
headers={
    "content-type": "application/json",
    "accept": "application/json",
    }

for k,v in enumerate(input_data):
    data = json.dumps(v)
    resp = requests.post(
        url=f"{api_base_url}{api_path}",
        headers=headers,
        auth=(api_client_id, api_api_key),
        data=data,
        )
        
    amp_group_create_res(k, v)

