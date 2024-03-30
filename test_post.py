import requests
import json

post = requests.post('https://fyp-server-django.onrender.com/api/data/gsm/', json=json.dumps({'name': 'leon'}))

print(post.status_code)