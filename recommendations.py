from pickle import load
from io import BytesIO
from requests import get
from cachetools import cached, TTLCache
from kaggle import KaggleApi

cache = TTLCache(maxsize=128, ttl=86400)


@cached(cache)
def getDataFromKaggle():
    api = KaggleApi()
    api.authenticate()
    link = api.kernel_output(user_name='rohankaran', kernel_slug='mrs-csv')
    response = get(link['files'][0]['url'])
    content = response.content
    result = load(BytesIO(content))
    return result


def getRecommendations(movie_schema):
    recommendations_list = getDataFromKaggle()
    if recommendations_list[int(movie_schema["id"])][1] == movie_schema["tconst"]:
        return recommendations_list[int(movie_schema["id"])][2]


@cached(cache)
def latest():
    api = KaggleApi()
    api.authenticate()
    link = api.kernel_output(user_name='rohankaran', kernel_slug='mrs-csv')
    response = get(link['files'][1]['url'])
    content = response.content
    result = load(BytesIO(content))
    return result
