import pickle

NEWS_LIMIT = 100
NEWS_LIST_BATCH_SIZE = 10

def getNewsSummariesForUser(user_id, page_num):
    page_num = int (page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    sliced_news = []

    if redis_client.get(user_id) is not None:
        # using pickle.loads convert string to json or dictionary
        news_digests = pickle.loads(redis_client.get(user_id))

        sliced_news_digests = news_digests[begin_index: end_index]

        db = mongodb_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest': {'$in': sliced_news_digests}}))
    else:
        db = mongodb_client.get_db()
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)])).limit(NEWS_LIMIT)