import requests

url = 'http://localhost:5000/results'
r = requests.post(url, json={'yourPL': 'spotify:playlist:18OPs73tK3BYXlwq4iCW3z'})

print(r.json())
