import requests
import urllib3
import json
import pprint
from decouple import config

# Import common code snippets, helpers from 'tools/common' parent folder
#   - Add 'tools/common/' to PYTHONPATH (shell: export, vscode: in .env file in workspace root)
#   - OR
#   - Copy the below ref 'from' modules directly in this folder
from yaml_from_excel_as_json import yaml_from_excel_as_json


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#### Firepower API access setup
fp_platform_url = "https://fmcrestapisandbox.cisco.com/api/fmc_platform/v1"
fp_config_url = "https://fmcrestapisandbox.cisco.com/api/fmc_config/v1/domain"

# get auth token
url = f"{fp_platform_url}/auth/generatetoken"
headers={
    "content-type": "application/json",
    "accept": "application/json",
}
data={}
auth = (config('FIREPOWER_API_USER'), config('FIREPOWER_API_PASS'))
resp = requests.post(
    url=url, 
    headers=headers, 
    data=data, 
    auth=auth,
    verify=False
)

if resp.status_code != 204:
    print(
        f"ERROR: {resp.status_code} - {resp.reason}. "+
        f"Failed to obtain firepower token.",
    )
    exit()

fp_access_token = resp.headers["x-auth-access-token"]
fp_refresh_token = resp.headers["x-auth-refresh-token"]
fp_global_domain_uuid = resp.headers["DOMAIN_UUID"]
fp_api_header={
    "content-type": "application/json",
    "accept": "application/json",
    "x-auth-access-token":fp_access_token,
}


#### Firepower - create new network/host/fqdn/range/url objects
# Read YAML data from Excel worksheet
input_data = yaml_from_excel_as_json(
    wbn="cisco_firepower.xlsx",
    wsn="obj_network_url",
    col_yaml_name="_yaml",
    )

# rest api call
headers = fp_api_header

for k,v in enumerate(input_data):
    if v["type"] == "Network":
        url = f"{fp_config_url}/{fp_global_domain_uuid}/object/networks?bulk=False"
    elif v["type"] == "Host":
        url = f"{fp_config_url}/{fp_global_domain_uuid}/object/hosts?bulk=False"
    elif v["type"] == "FQDN":
        url = f"{fp_config_url}/{fp_global_domain_uuid}/object/fqdns?bulk=False"
    elif v["type"] == "Range":
        url = f"{fp_config_url}/{fp_global_domain_uuid}/object/ranges?bulk=False"
    elif v["type"] == "Url":
        url = f"{fp_config_url}/{fp_global_domain_uuid}/object/urls?bulk=False"
    else:
        print(f"Skipped: {v['name']} due to invalid type {v['type']}")
        continue
    
    data = json.dumps(v)
    resp = requests.post(
        url=url, 
        headers=headers, 
        data=data, 
        verify=False,
    )
    
    if resp.status_code == 201:
        id = resp.json()["id"]
        print(f"OK: {v['name']} of type {v['type']} created. ID = {id}")
    else:
        err = resp.json()["error"]["messages"][0]["description"]
        print(
            f"ERROR: {resp.status_code} - {resp.reason}. "+
            f"Failed to create object {v['name']}. {err}",
        )


#### Firepower - create new network/host/fqdn/range/url objects GROUPS
# Read YAML data from Excel worksheet
input_data = yaml_from_excel_as_json(
    wbn="cisco_firepower.xlsx",
    wsn="obj_group_network_url",
    col_yaml_name="_yaml",
    )

# rest api call
headers = fp_api_header

for k,v in enumerate(input_data):
    if v["type"] == "NetworkGroup":
        url = f"{fp_config_url}/{fp_global_domain_uuid}/object/networkgroups?bulk=False"
    elif v["type"] == "UrlGroup":
        url = f"{fp_config_url}/{fp_global_domain_uuid}/object/urlgroups?bulk=False"
    else:
        print(f"Skipped: {v['name']} due to invalid type {v['type']}")
        continue
    
    # Remove partial / blank list items, where dict is incomplete or value is None
    v["literals"] = list(map(lambda x: x if "value" in x or "url" in x else None, v["literals"]))
    v["literals"] = list(filter(lambda x: True if x is not None else False, v["literals"]))
    
    data = json.dumps(v)
    # print(v) & exit()
    resp = requests.post(
        url=url, 
        headers=headers, 
        data=data, 
        verify=False,
    )
    
    if resp.status_code == 201:
        id = resp.json()["id"]
        print(f"OK: {v['name']} of type {v['type']} created. ID = {id}")
    else:
        err = resp.json()["error"]["messages"][0]["description"]
        print(
            f"ERROR: {resp.status_code} - {resp.reason}. "+
            f"Failed to create object {v['name']}. {err}",
        )
        
