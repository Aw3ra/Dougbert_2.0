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
            twttr_search_tweets.get_notifications()
        except Exception as e:
            print('Error in search_tweets: '    + str(e), flush=True)

def respond_to_notification():
    with lock:
        try:
            responding.respond_to_notification()
            print('Responded to notification', flush=True)
        except Exception as e:
            print('Error in respond_to_notification: '    + str(e), flush=True)

def main():
    # Use this to load environment variables from .env file
    load_dotenv()
    notif_search_time =  int(os.getenv('NOTIFICATION_SEARCH_TIME'))
    respond_time = int(os.getenv('RESPOND_TIME'))
    search_tweets()
    respond_to_notification()
    schedule.every(notif_search_time).minutes.do(search_tweets)
    schedule.every(respond_time).minutes.do(respond_to_notification)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()