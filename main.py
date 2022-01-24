import requests
import json


url = 'https://api.github.com'
user = 'Novopashin-GS'
response = requests.get(f'{url}/users/{user}/repos').json()
with open('data.json', 'w', encoding='UTF-8') as data:
    json.dump(response, data)


