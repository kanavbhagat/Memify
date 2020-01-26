import requests

api_key = "dc6zaTOxFJmzC"

params = {'q': "query",'api_key': api_key,'limit': 3,'rating': 'pg'}
r = requests.get("http://api.giphy.com/v1/gifs/search", params=params)
data = r.json()['data']
print(data)