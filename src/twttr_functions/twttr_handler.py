from .functions import get_tweet, get_tweet_conversation, post_alternatate, retweet_tweet, like_tweet, login_alternate, get_timeline_tweets
import os

SESSION = os.getenv("DOUGBERT_SESSION")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")



def decide_action(action, tweet_id = None, tweet = None, email = None, password = None):
    if action == 'like':
        like_tweet.like_tweet(tweet_id, SESSION, RAPID_API_KEY)
    elif action == 'retweet':
        retweet_tweet.retweet_tweet(tweet_id, SESSION, RAPID_API_KEY)
    elif action == 'tweet':
        post_alternatate.post_tweet(tweet, SESSION, RAPID_API_KEY, in_reply_to_status_id=tweet_id)
    elif action == 'conversation':
        return get_tweet.get_tweet_conversation(tweet_id, RAPID_API_KEY)
    elif action == 'log-in':
        return login_alternate.login_to_twitter(email, password, RAPID_API_KEY)
    elif action == 'get-tweet':
        return get_tweet.get_tweet(tweet_id, RAPID_API_KEY)
    elif action == 'random-timeline':
        return get_timeline_tweets.get_tweet(RAPID_API_KEY, SESSION)
    # elif action == 'get-dms':
    #     return get_dms.get_dms(SESSION, RAPID_API_KEY)
    else:
        return 'Invalid action'


# if __name__ == '__main__':
#     print(decide_action('get-dms', SESSION, RAPID_API_KEY))