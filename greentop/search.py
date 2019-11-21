 
import requests
import json

url = 'http://localhost:9080/crawl.json?start_requests=true&spider_name=green_top'
headers = {'Content-Type': 'application/json'}

filters = [dict(name="Product_Name", op="equals_to", val="%Smith's%",single=True,limit=1)]
params = dict(q=json.dumps(dict(filters=filters)))

response = requests.get(url, params=params, headers=headers)
assert response.status_code == 200
print(response.json())

