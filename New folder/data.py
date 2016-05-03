import requests
import time
import math
import pickle
import pandas as pd

# Get most popular TV shows or Movies
api_key = input('Enter API key: ')


def popular_titles(n, movie_or_tv = 'tv'):
    """Returns n most popular in a list"""
    url = 'https://api.themoviedb.org/3/{}/popular'.format(movie_or_tv)
    pages = math.ceil(n/20)  # each page gives 20 titles
    page = 1
    titles = []
    while page <= pages:  # iterate through pages to get titles
        payload = {'api_key': api_key, 'page': page}
        r = requests.get(url, params=payload)
        if r.status_code == 200:
            titles.extend(r.json()['results'])
            print('Fetching page ', page)
            page += 1
        if r.status_code == 429:  # Status code for too many requests
            print('Tried Page {}. Too many requests, waiting for 2 seconds...'.format(page))
            time.sleep(0.05)
    print('done')
    return titles[0:n]

df = pd.DataFrame(shows)
df.to_pickle('data.pkl')