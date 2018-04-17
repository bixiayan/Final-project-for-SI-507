# imdbID year score actors directors genre ratings, rank
# {"Title":"Carmencita",
# "Year":"1894",
# "Rated":"NOT RATED",
# "Released":"10 Mar 1894",
# "Runtime":"1 min",
# "Genre":"Documentary, Short",
# "Director":"William K.L. Dickson",
# "Writer":"N/A","Actors":"Carmencita",
# '''
# "Plot":"Performing on what looks like a small wooden stage, wearing a dress with a hoop skirt and white high-heeled pumps, 
# Carmencita does a dance with kicks and twirls, a smile always on her face.",
# '''
# "Language":"N/A",
# "Country":"USA",
# "Awards":"N/A",
# "Poster":"https://images-na.ssl-images-amazon.com/images/M/MV5BMjAzNDEwMzk3OV5BMl5BanBnXkFtZTcwOTk4OTM5Ng@@._V1_SX300.jpg",
# "Ratings":[{"Source":"Internet Movie Database","Value":"5.8/10"}],
# "Metascore":"N/A","imdbRating":"5.8","imdbVotes":"1,263","imdbID":"tt0000001",
# "Type":"movie","DVD":"N/A",
# "BoxOffice":"N/A",
# "Production":"N/A",
# "Website":"N/A",
# "Response":"True"}

# "http://www.omdbapi.com/?s=Paris pieds nus": "{\"Response\":\"False\",\"Error\":\"Movie not found!\"}", 
# "http://www.omdbapi.com/?s=Bahubali: The Beginning": "{\"Response\":\"False\",\"Error\":\"Movie not found!\"}", 

# # table basic info
# imdbID year actors directors genre description
# imdbID score, ratings, rank
import sqlite3
import csv
import json
import ast
import secrets
import requests

key = secrets.key
DBNAME = 'movies.db'
MOVIECSV = 'IMDB-Movie-Data.csv'
JSON = 'cache.json'
CACHE_FNAME = "imdb.json"


try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}


def get_unique_key(url):
  return url

# The main cache function: it will always return the result for this
# url+params combo. However, it will first look to see if we have already
# cached the result and, if so, return the result from cache.
# If we haven't cached the result, it will get a new one (and cache it)

def make_request_using_cache(url):
    params = {'apikey': key}
    unique_ident = get_unique_key(url)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url, params)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]




def one_thousand_movies(json_file):
    data = json.load(open(json_file))
    imdb_ids = []
    for key, value in data.items():
        value = ast.literal_eval(value)
        if 'Search' in value:
            item = value['Search'][0]
            imdb_ids.append(item['imdbID'])

    base_url = "http://www.omdbapi.com/?i="
    for id in imdb_ids:
        url = base_url + str(id)
        data = make_request_using_cache(url)

    

if __name__=="__main__":
    one_thousand_movies(JSON)


































