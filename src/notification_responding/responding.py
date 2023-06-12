import json
from commands import decide_command
from twttr_functions import twttr_handler
from openAI import create_tweet_response
from data_ingestion import request_info
import re
import time
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import random





def perform_action(action, tweet_conversation, tweet_id = None):
    try:
        # If the last tweet in the conversation is a message by the bot, ignore it
        if not tweet_conversation[-1]['content'].startswith(os.getenv("TWITTER_HANDLE")):
            if action == 'B':
                # Create ai response first
                tweet_response = create_tweet_response.build_message(tweet_conversation)
                twttr_handler.decide_action('tweet', tweet = tweet_response, tweet_id = tweet_id)
            elif action == 'C':
                twttr_handler.decide_action('retweet', tweet_id = tweet_id)
            elif action == 'D':
                twttr_handler.decide_action('like', tweet_id = tweet_id)
            elif action == 'E':
                print('Follow user')
            elif action == 'F':
                # Create ai response first
                tweet_response = create_tweet_response.build_message(tweet_conversation, prior_known_info = request_info.return_system_message(tweet_conversation))
                twttr_handler.decide_action('tweet', tweet = tweet_response, tweet_id = tweet_id)
            elif action == 'G':
                print('Check Solana price')
            elif action == 'H':
                print('Lookup user profile')
            elif action == 'I':
                print('Sending tip')
                # Create message along with the tip
                tweet_response = create_tweet_response.build_tip_message(tweet_conversation)
                # To user name is the last user name in the thread
                return twttr_handler.decide_action('send-dm', tweet = tweet_response, to_user_name = tweet_conversation[-1]['content'].split(':')[0])
        else:
            print('Last tweet in conversation is by bot, ignoring')
    except Exception as e:
        raise e

def respond_to_notification():
    load_dotenv()
    client = MongoClient(os.getenv("DATABASE_URL"))
    with open('src/profile.json', 'r', encoding='utf-8') as f:
        records = json.load(f)['config_data']
        database = records["Database_records"]['Database']
        collection = records["Database_records"]["Collection"]
        notifications_collection = client[database][collection]

    # Function to update actioned to true
    def update_actioned(tweet):
        result = notifications_collection.update_one({"tweetId": tweet}, {"$set": {"actioned": True}})

    def get_tweet():
        tweets = list(notifications_collection.find({"actioned": False}))
        tweets.reverse()
        if len(tweets) == 0:
            return None
        return tweets[0]


    # 50/50 chance of getting a notification tweet or a random tweet
    update_database = False
    if random.randint(0,10) == 0:
        tweet = twttr_handler.decide_action('random-timeline')
    else:
        tweet = get_tweet()
        if tweet == None:
            tweet = twttr_handler.decide_action('random-timeline')
        else:
            tweet = tweet['tweetId']
            update_database = True

    try:
        if tweet == None:
            return
        tweet_conversation = twttr_handler.decide_action('conversation', tweet_id = tweet)
        print(tweet_conversation)
        if len(tweet_conversation) != 0:
            actions = decide_command.decide_command(tweet_conversation)
            actions_list = [action.strip() for action in re.search(r"\[(.*?)\]", actions).group(1).split(',')]
            if 'A' not in actions_list:
                perform_action('B', tweet_conversation, tweet_id=tweet)
                # for action in actions_list:
                #     perform_action(action, tweet_conversation, tweet_id=tweet)
            else:
                print('Do nothing')

    except Exception as e:
        print(f'Error in respond_to_notification: {e}')
    finally:
        if update_database:
            update_actioned(tweet)
        time.sleep(20) 


def testing():
    # tweet_conversation = twttr_handler.decide_action('conversation', tweet_id = "1664497913299632128")
    print(twttr_handler.decide_action('send-dm', tweet = 'Thankyou so much for interacting with me! Here\'s a little tip for your time!', to_user_name = '_qudo'))
    # return perform_action('I', tweet_conversation)

# twitter_handler.decide_action('reply_to_tweet', tweet = 'Test tweet', tweet_id = asyncio.run(get_tweet()).tweetId)


