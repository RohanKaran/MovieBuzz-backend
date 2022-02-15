import datetime
import time
from io import BytesIO
from urllib.error import HTTPError
from urllib.request import urlopen, Request
from requests import get
import json
import os
import ssl
from cachetools import cached, TTLCache
from kaggle import KaggleApi
from pandas import read_csv

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

    url = 'http://2b9e4c43-ad5c-491e-8c0a-b81746d0a5d2.centralus.azurecontainer.io/score'
    api_key = 'ZMGjhb6sGQYUyWnxeU8Phbp4Is1QDm6T'  # Replace this with the API key for the web service
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

    req = Request(url, body, headers)

    try:
        response = urlopen(req)
        result = response.read()
        result = json.loads(result)
        print(time.time() - start)
        return result['Results']['output1']
    except HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))


cache = TTLCache(maxsize=1, ttl=86400)


@cached(cache)
def latest():
    api = KaggleApi()
    api.authenticate()
    link = api.kernel_output(user_name='rohankaran', kernel_slug='mrs-csv')
    response = get(link)
    content = response.content
    f = read_csv(BytesIO(content))

    allm = f['primaryTitle'].tolist()

    trending_movies = f[(f.startYear >= datetime.date.today().year - 1) & (f.titleType == "['movie']")]
    trending_movies = trending_movies.sort_values(['popularity'], ascending=False).head(10).tconst.tolist()
    trending_series = f[(f.startYear >= datetime.date.today().year - 1) & (f.titleType == "['tvSeries']")]
    trending_series = trending_series.sort_values(['popularity'], ascending=False).head(10).tconst.tolist()

    top_movies = f.sort_values(['popularity'], ascending=False).head(10).tconst.tolist()
    top_series = f.sort_values(['popularity'], ascending=False).head(10).tconst.tolist()

    return {"all": allm, "trm": trending_movies, "trs": trending_series, "tm": top_movies, "ts": top_series}
