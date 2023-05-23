from notification_responding import responding
from notification_saving import twttr_search_tweets
from new_engagement import post_new
import schedule
import time
import threading

lock = threading.Lock()

notif_search_time = 10
respond_time = 1
post_time = 30

# Every 10 minutes try to save new tweets


def search_tweets():
    with lock:
        try:
            print('Searching for tweets')
            twttr_search_tweets.get_notifications()
        except Exception as e:
            print('Error in search_tweets: '    + str(e))

def respond_to_notification():
    with lock:
        try:
            print('Responding to notifications')
            responding.respond_to_notification()
        except Exception as e:
            print('Error in respond_to_notification: '    + str(e))

def post_new_tweet():
    with lock:
        try:
            print('Posting new tweet')
            post_new.post_tweet()
        except Exception as e:
            print('Error in post_new_tweet: '    + str(e))


def main():
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