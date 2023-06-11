import os
import dotenv
import asyncio
from commands import decide_command
from twttr_functions import twttr_handler
from openAI import create_tweet_response
from data_ingestion import request_info
from pymongo import MongoClient
import re
import time




def perform_action(action, tweet_conversation, tweet_id = None):
    try:
        if action == 'B':
            # Create ai response first
            tweet_response = create_tweet_response.build_message(tweet_conversation)
            print(tweet_response)
            twttr_handler.decide_action('tweet', tweet = tweet_response, tweet_id = tweet_id)
        elif action == 'C':
            twttr_handler.decide_action('retweet', tweet_id = tweet_id)
            print('Retweeted tweet')
        elif action == 'D':
            twttr_handler.decide_action('like', tweet_id = tweet_id)
            print('Liked tweet')
        elif action == 'E':
            print('Follow user')
    except Exception as e:
        raise e

def respond_to_notification():
    dotenv.load_dotenv()
    client = MongoClient(os.getenv("DATABASE_URL"))
    db = client["Shrempbrain_prod"]
    notifications_collection = db["notifications"]

    def update_actioned(tweet):
        notifications_collection.update_one({"_id": tweet["_id"]}, {"$set": {"actioned": True}})

    def get_tweets():
        tweets = list(notifications_collection.find({"actioned": False}))
        tweets.reverse()
        if len(tweets) == 0:
            return None
        return tweets

    tweets = get_tweets()
    if tweets is not None:
        for tweet in tweets:
            try:
                if tweet is None:
                    return
                tweet_conversation = twttr_handler.decide_action('conversation', tweet_id=tweet["_id"])
                if len(tweet_conversation) != 0:
                    actions = decide_command.decide_command(tweet_conversation)
                    print(actions)
                    actions_list = [action.strip() for action in re.search(r"\[(.*?)\]", actions).group(1).split(',')]
                    if 'A' not in actions_list:
                        for action in actions_list:
                            perform_action(action, tweet_conversation, tweet_id=tweet["_id"])
                    else:
                        print('Do nothing')

            except Exception as e:
                print(f'Error in respond_to_notification: {e}')
                raise e
            finally:
                update_actioned(tweet)
                time.sleep(20)
    else:
        print('No tweets to respond to')


def testing():
    tweet_conversation = twttr_handler.decide_action('conversation', tweet_id = "1664497913299632128")
    return perform_action('I', tweet_conversation)

# twitter_handler.decide_action('reply_to_tweet', tweet = 'Test tweet', tweet_id = asyncio.run(get_tweet()).tweetId)


