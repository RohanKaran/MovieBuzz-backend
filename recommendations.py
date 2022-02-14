import datetime
import time
from urllib.error import HTTPError
from urllib.request import urlopen, Request
import json
import os
import ssl
from cachetools import cached, TTLCache
from kaggle import KaggleApi
import pandas as pd

start = time.time()


def getRecommendations(movie_name):
    def allowSelfSignedHttps(allowed):
        # bypass the server certificate verification on client side
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context

    allowSelfSignedHttps(True)  # this line is needed if you use self-signed certificate in your scoring service.

    # Request data goes here
    data = {
        "Inputs": {
            "input1":
                [
                    {
                        "Col1": movie_name
                    },
                ]
        },
        "GlobalParameters": {
        }
    }

    body = str.encode(json.dumps(data))
    print(body)
    url = 'http://e626eedc-13f8-40ef-869a-a714a3ab3872.centralus.azurecontainer.io/score'
    api_key = 'YiXONYhTdkJcMHEccvHAAWYE6cNUmyiF'  # Replace this with the API key for the web service
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

    req = Request(url, body, headers)

    try:
        response = urlopen(req)

        result = response.read()
        result = json.loads(result)
        return result['Results']['output1']
    except HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))

    print(time.time() - start)


cache = TTLCache(maxsize=1, ttl=86400)


def latest():
    api = KaggleApi()
    api.authenticate()
    link = api.kernel_output(user_name='rohankaran', kernel_slug='mrs-csv')
    f = pd.read_csv(urlopen(link['files'][0]['url']))

    allm = f['tconst'].values

    trending_movies = f[(f.startYear >= datetime.date.today().year - 1) & (f.titleType == "['movie']")]
    trending_movies = trending_movies.sort_values(['popularity'], ascending=False).head(10).tconst.values
    trending_series = f[(f.startYear >= datetime.date.today().year - 1) & (f.titleType == "['tvSeries']")]
    trending_series = trending_series.sort_values(['popularity'], ascending=False).head(10).tconst.values

    top_movies = f.sort_values(['popularity'], ascending=False).head(10).tconst.values
    top_series = f.sort_values(['popularity'], ascending=False).head(10).tconst.values

    return {"all": allm, "trm": trending_movies, "trs": trending_series, "tm": top_movies, "ts": top_series}
