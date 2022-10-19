from pickle import load
from io import BytesIO
from requests import get
from cachetools import cached, TTLCache
from kaggle import KaggleApi

cache1 = TTLCache(maxsize=128, ttl=80000)
cache2 = TTLCache(maxsize=128, ttl=80000)


@cached(cache1)
def getDataFromKaggle():
    api = KaggleApi()
    api.authenticate()
    link = api.kernel_output(user_name='rohankaran', kernel_slug='movie-recommendation-system')
    response = get(link['files'][0]['url'])
    content = response.content
    result = load(BytesIO(content))
    return result


def getRecommendations(movie_schema):
    recommendations_list = getDataFromKaggle()
    if recommendations_list[int(movie_schema["id"])][1] == movie_schema["tconst"]:
        return recommendations_list[int(movie_schema["id"])][2]


@cached(cache2)
def latest():
    api = KaggleApi()
    api.authenticate()
    link = api.kernel_output(user_name='rohankaran', kernel_slug='movie-recommendation-system')
    response = get(link['files'][1]['url'])
    content = response.content
    result = load(BytesIO(content))
    return result
