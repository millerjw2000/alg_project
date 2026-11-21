import requests

url = 'https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/seasons/2026/teams'
#response = urllib.request.urlopen(url)
#content = response.json()
#for key in content:
#    print(key)

response = requests.get(url)
data = response.json()

for item in data['items']:

    print(item['$ref'])