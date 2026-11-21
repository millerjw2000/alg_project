import requests
import sqlite3

url = 'https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/seasons/2026/teams'
#response = urllib.request.urlopen(url)
#content = response.json()
#for key in content:
#    print(key)

# response = requests.get(url)
# data = response.json()

# for item in data['items']:

#     print(item['$ref'])

def insert_team(info):

    pass

def get_connection():
    conn = sqlite3.connect('data/stats.db')
    return conn

def main():
    pass

if __name__ == '__main__':

    main()