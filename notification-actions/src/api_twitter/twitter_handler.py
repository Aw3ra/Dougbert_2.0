from .twitter_commands import post_tweet, like_tweet, retweet_tweet, full_thread
import os
import tweepy

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")

# Function to decide which function to call
# Inputs:   action - the action to take, follow or unfollow
#           kwargs - the additional info required for the action
# Outputs:  None
def decide_action(action, **kwargs):
        # Set up tweepy client
        posting_client = tweepy.Client(  
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_TOKEN, 
            access_token_secret= ACCESS_TOKEN_SECRET
        )
        # 

        # Call the appropriate function based on the action
        match action:
            case 'tweet':
                return post_tweet.post_tweet(posting_client, kwargs['tweet'])
            case 'reply_to_tweet':
                return post_tweet.post_tweet(posting_client, kwargs['tweet'], tweet_ID = kwargs['tweet_id'])
            case 'like':
                return like_tweet.like_tweet(posting_client, kwargs['tweet_id'])
            case 'retweet':
                return retweet_tweet.retweet_tweet(posting_client, kwargs['tweet_id'])
            case 'full_thread':
                return full_thread.full_thread(posting_client, kwargs['tweet_id'])
            case _:
                return 'Invalid action'
