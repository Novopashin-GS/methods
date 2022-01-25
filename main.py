import requests
import json


url = 'https://api.github.com'
user = 'Novopashin-GS'
response = requests.get(f'{url}/users/{user}/repos').json()
with open('data.json', 'w', encoding='UTF-8') as data:
    json.dump(response, data)

#vk
with open('token.json', 'r', encoding='UTF-8') as token:
    access_token = json.load(token)['access_token']
url = 'https://api.vk.com/method/groups.get'
params = {
    'user_id': 305438274,
    'access_token': access_token,
    'v': 5.131,
    'extended': 1
}
response = requests.get(url, params=params)
print(response.json())


