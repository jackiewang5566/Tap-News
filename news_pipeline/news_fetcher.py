import os
import sys

from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

DEDUPE_NEWS_TASK_QUEUE_URL = 'amqp://sspuqxlv:su5SdhMPn-x2lnKElijEbGxLEGpZxtRT@wasp.rmq.cloudamqp.com/sspuqxlv'
DEDUPE_NEWS_TASK_QUEUE_NAME = 'tap-news-dedupe-news-task-queue'
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://mcyrgohw:CB44sIsZxuz-IInG5a5ESFGrnP0iIda4@crane.rmq.cloudamqp.com/mcyrgohw"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print 'message is broken'
        return

    task = msg
    text = None

    # if task['source'] == 'cnn':
    #     print 'scraping CNN news'
    #     text = cnn_news_scraper.extract_news(task['url'])
    # else:
    #     print 'news source [%s] is not supported.' % task['source']
    
    # task['text'] = text

    article = Article(task['url'])
    article.download()
    article.parse()

    # article.text is unicode, need to encode it to utf-8
    task['text'] = article.text.encode('utf-8')

    dedupe_news_queue_client.send_message(task)

while True:
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.get_message()
        if msg is not None:
            try:
                handle_message(msg)
            except Exception as e:
                print e
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)

