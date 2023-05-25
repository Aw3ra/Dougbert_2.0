from prisma import Client
import asyncio
from commands import decide_command
from twttr_functions import twttr_handler
from openAI import create_tweet_response
from data_ingestion import request_info
import re
import time


prisma_client = Client()

def perform_action(action, tweet_conversation, tweet_id = None):
    try:
        if action == 'B':
            # Create ai response first
            tweet_response = create_tweet_response.build_message(tweet_conversation, prior_known_info = request_info.return_system_message(tweet_conversation))
            print(tweet_response)
            twttr_handler.decide_action('tweet', tweet = tweet_response, tweet_id = tweet_id)
            print('Replied to tweet')
        elif action == 'C':
            twttr_handler.decide_action('retweet', tweet_id = tweet_id)
            print('Retweeted tweet')
        elif action == 'D':
            twttr_handler.decide_action('like', tweet_id = tweet_id)
            print('Liked tweet')
        elif action == 'E':
            print('Follow user')
        elif action == 'F':
            print('Search the internet')
            # Create ai response first
            tweet_response = create_tweet_response.build_message(tweet_conversation, prior_known_info = request_info.return_system_message(tweet_conversation))
            twttr_handler.decide_action('tweet', tweet = tweet_response, tweet_id = tweet_id)
        elif action == 'G':
            print('Check Solana price')
        elif action == 'H':
            print('Lookup user profile')
    except Exception as e:
        raise e

def respond_to_notification():
    async def update_actioned(tweet):
        await prisma_client.connect()
        await prisma_client.notification.update(where = {"tweetId": tweet.tweetId}, data = {"actioned": True})
        await prisma_client.disconnect()

    async def get_tweet():
        await prisma_client.connect()
        tweets = await prisma_client.notification.find_many(where = {"actioned": False})
        await prisma_client.disconnect()
        tweets.reverse()
        if len(tweets) == 0:
            return None
        return tweets
    tweets = asyncio.run(get_tweet())
    if tweets != None:
        for tweet in tweets:
            try:
                if tweet == None:
                    return
                tweet_conversation = twttr_handler.decide_action('conversation', tweet_id = tweet.tweetId)
                if len(tweet_conversation) != 0:
                    actions = decide_command.decide_command(tweet_conversation)
                    print(actions)
                    actions_list = [action.strip() for action in re.search(r"\[(.*?)\]", actions).group(1).split(',')]
                    if 'A' not in actions_list:
                        for action in actions_list:
                            perform_action(action, tweet_conversation, tweet_id=tweet.tweetId)
                    else:
                        print('Do nothing')
                
            except Exception as e:
                print(f'Error in respond_to_notification: {e}')
                raise e
            finally:
                asyncio.run(update_actioned(tweet))
                time.sleep(20)
    else:
        print('No tweets to respond to')




# twitter_handler.decide_action('reply_to_tweet', tweet = 'Test tweet', tweet_id = asyncio.run(get_tweet()).tweetId)


