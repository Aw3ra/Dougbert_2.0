#!/usr/bin/env python3
from notification_responding import responding
from notification_saving import twttr_search_tweets
from new_engagement import post_new
import schedule
import time
import threading
import os
from dotenv import load_dotenv



lock = threading.Lock()

# Every 10 minutes try to save new tweets


def search_tweets():
    with lock:
        try:
            print('Searching for tweets', flush=True)
            twttr_search_tweets.get_notifications()
        except Exception as e:
            print('Error in search_tweets: '    + str(e), flush=True)

def respond_to_notification():
    with lock:
        try:
            print('Responding to notifications', flush=True)
            responding.respond_to_notification()
        except Exception as e:
            print('Error in respond_to_notification: '    + str(e), flush=True)

def post_new_tweet():
    with lock:
        try:
            print('Posting new tweet', flush=True)
            post_new.post_tweet()
        except Exception as e:
            print('Error in post_new_tweet: '    + str(e), flush=True)


def main():
    # Use this to load environment variables from .env file
    load_dotenv()
    notif_search_time =  int(os.getenv('NOTIFICATION_SEARCH_TIME'))
    respond_time = int(os.getenv('RESPOND_TIME'))
    post_time = int(os.getenv('POST_TIME'))
    print('Starting initial search, response, and post', flush=True)
    search_tweets()
    respond_to_notification()
    post_new_tweet()
    schedule.every(notif_search_time).minutes.do(search_tweets)
    schedule.every(respond_time).minutes.do(respond_to_notification)
    schedule.every(post_time).minutes.do(post_new_tweet)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()