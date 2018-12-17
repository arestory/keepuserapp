import requests
import json

f = requests.get('http://wanandroid.com/wxarticle/chapters/json')
data = json.loads(f.content)['data']
for d in data:
    print(d['name'])