import pickle
import networkx as nx
import tvNetwork as tvn
import requests
import time
import pandas as pd

# Set up for tmdb api calls
api_key = input('Enter API key: ')
payload = {'api_key': api_key}

# get the 'last' show id using the 'latest call'
last_id = requests.get(url = 'https://api.themoviedb.org/3/tv/latest', params=payload).json()['id']

# get individual show info by seqeuntially iterating from 1 through last_id
shows = []
id = 1
index = 0
while id <= last_id:
    url = 'https://api.themoviedb.org/3/tv/{}'.format(id)  # for main info
    url2 = 'https://api.themoviedb.org/3/tv/{}/keywords'.format(id)  # for keywords of the show
    r = requests.get(url, params=payload)
    r2 = requests.get(url2, params=payload)
    if r.status_code == 200 & r2.status_code == 200:
        shows.append(r.json())
        shows[index].update({'keywords': r2.json()['results']})
        print('Fetching Show {} of {}'.format(id, last_id))
        id += 1
        index += 1
    if r.status_code == 429 or r2.status_code == 429:
        print('Tried show {} of {}...Sleeping for 1 second'.format(id, last_id))
        time.sleep(1)
    if r.status_code == 404 or r2.status_code == 404:
        print('Show {} does not exist'.format(id))
        id += 1
print('done')

output = open('all_shows.pkl', 'wb')
pickle.dump(shows, output)
output.close()

df = pd.DataFrame(shows)
pd.to_pickle(df, 'shows_df.pkl')



