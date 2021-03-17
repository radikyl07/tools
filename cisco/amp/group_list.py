import requests
from decouple import config


#### Get groups
#TODO: Limit and Pagination considerations

api_base_url = 'https://api.apjc.amp.cisco.com/v1/'
api_client_id = config('AMP_CLIENT_ID')
api_api_key = config('AMP_API_KEY')
api_path = "groups"
headers={
    "content-type": "application/json",
    "accept": "application/json",
}

resp = requests.get(
    url=api_base_url+api_path,
    headers=headers,
    auth=(api_client_id, api_api_key),
)

data = resp.json()
recs = data['metadata']['results']['total']
    
print(f"TOTAL GROUPS: {recs}")
print("name, description, guid, source")
for d in data["data"]:
    print(f"{d['name']}, {d['description']}, {d['guid']}, {d['source']}")
