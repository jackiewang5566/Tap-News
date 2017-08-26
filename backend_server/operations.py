import json
import os
import pickle
import random
import redis
import sys

from bson.json_util import dumps
from datetime import datetime

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
# import news_recommendation_service_client

from cloudAMQP_client import CloudAMQPClient

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

NEWS_TABLE_NAME = 'news'
CLICK_LOGS_TABLE_NAME = 'click_logs'

NEWS_LIMIT = 100
NEWS_LIST_BATCH_SIZE = 10
USER_NEWS_TIME_OUT_IN_SECONDS = 60

# LOG_CLICKS_TASK_QUEUE_URL = 
# LOG_CLICKS_TASK_QUEUE_NAME = 

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)
# cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)


def getNewsSummariesForUser(user_id, page_num):
    page_num = int (page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    # The final list of news to be returned
    sliced_news = []

    if redis_client.get(user_id) is not None:
        # using pickle.loads convert string to pickled object
        news_digests = pickle.loads(redis_client.get(user_id))
        
        # if begin_index is out of range, this will return empty list;
        # if end_index is out of range (begin_index is within the range), this 
        # will return all remaining news ids.
        sliced_news_digests = news_digests[begin_index:end_index]
        print sliced_news_digests
        db = mongodb_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest': {'$in': sliced_news_digests}}))
    else:
        db = mongodb_client.get_db()
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        total_news_digests = map(lambda x:x['digest'], total_news)
        # in redis, usually use pickle instead of json package
        redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)
        sliced_news = total_news[begin_index:end_index]

    for news in sliced_news:
        # Remove text field to save bandwidth
        del news['text']
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'
    
    # sliced_news is a pickle object, it needs to dumps to json before return to nodejs
    # dumps below is pickle.dumps
    return json.loads(dumps(sliced_news))