""" Client news api service """
import requests

from json import loads

NEWS_API_ENDPOINT = 'https://newsapi.org/v1/'
NEWS_API_KEY = '915949aa547549b3bb739f67d1391375'

ARTICLES_API = 'articles'

BBC_NEWS = 'bbc-news'
BBC_SPORT = 'bbc-sport'
CNN = 'cnn'

DEFAULT_SOURCES = [BBC_NEWS, CNN]
SORT_BY_TOP = 'top'


def buildUrl(endPoint=NEWS_API_ENDPOINT, apiName=ARTICLES_API):
    return endPoint + apiName


def getNewsFromSource(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):
    articles = []

    for source in sources:
        payload = {
            'apiKey': NEWS_API_KEY,
            'source': source,
            'sortBy': sortBy
        }
        # add verify=False using homebrew install python, then have ssl error issue
        response = requests.get(buildUrl(), params=payload, verify=False)

        print response.content
        res_json = loads(response.content)
        
        # Extract info from response
        if (res_json is not None and 
            res_json['status'] == 'ok' and 
            res_json['source'] is not None):
            # populate news source in each articles
            for news in res_json['articles']:
                news['source'] = res_json['source']

            articles.extend(res_json['articles'])


    return articles