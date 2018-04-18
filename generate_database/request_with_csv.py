import json
import secrets
import requests
import csv

class Movie:
    def __init__(self, name, year):
        self.name = name
        self.year = year

key = secrets.key
CACHE_FNAME = 'cache.json'
CSVFILE = "IMDB-Movie-Data.csv"

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





def make_one_thousand_movies(csv_file):
    movie_name_lists = []
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = True
        count = 1
        for row in reader:
            if header:
                header = False
                continue
            movie = Movie(row[1], row[6])
            movie_name_lists.append(movie)
    base_url = "http://www.omdbapi.com/?s="
    for movie in movie_name_lists:
        url = base_url + movie.name
        url += "&y=" + str(movie.year)
        data = make_request_using_cache(url)





if __name__ == "__main__":
    make_one_thousand_movies(CSVFILE)