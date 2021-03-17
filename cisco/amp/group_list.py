import requests
from decouple import config

#### Initialize

AMP_BASE_URL = 'https://api.apjc.amp.cisco.com/v1/'
AMP_CLIENT_ID = config('AMP_CLIENT_ID')
AMP_API_KEY = config('AMP_API_KEY')



#### Get groups
#TODO: Limit and Pagination considerations

headers={
    "content-type": "application/json",
    "accept": "application/json",
}

resp = requests.get(
    url=AMP_BASE_URL+"groups",
    headers=headers,
    auth=(AMP_CLIENT_ID, AMP_API_KEY),
)

data = resp.json()
recs = data['metadata']['results']['total']
    
print(f"TOTAL GROUPS: {recs}")
print("name, description, guid, source")
for d in data["data"]:
    print(f"{d['name']}, {d['description']}, {d['guid']}, {d['source']}")
