from .functions import get_tweet, get_tweet_conversation, post_alternatate, retweet_tweet, like_tweet, login_alternate, get_timeline_tweets, send_dm
import os
from dotenv import load_dotenv
import time





def decide_action(action, tweet_id = None, tweet = None, email = None, password = None, to_user_name = None, to_user_id = None, media_id = None):
    load_dotenv()
    SESSION = os.getenv("DOUGBERT_SESSION")
    RAPID_API_KEY = os.getenv("RAPID_API_KEY")
    retries = 5
    for i in range(retries):
        try:
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
            elif action == 'send-dm':
                return send_dm.send_dm(tweet, SESSION, RAPID_API_KEY, to_user_name=to_user_name, to_user_id=to_user_id, media_id=None)
            # elif action == 'get-dms':
            #     return get_dms.get_dms(SESSION, RAPID_API_KEY)
            else:
                return 'Invalid action'
        except Exception as e:
            if i < retries - 1:  # i starts at 0, so we subtract 1
                print('Error encountered performing: '+action, str(e))
                print(f'Retrying after 5 seconds... (Attempt {i+2}/{retries})')  # i+2 because i starts at 0
                time.sleep(5)
            else:
                print('Error encountered on the final attempt. No further retries will be made.')
                raise  # re-raise the last exception

# if __name__ == '__main__':
#     print(decide_action('get-dms', SESSION, RAPID_API_KEY))