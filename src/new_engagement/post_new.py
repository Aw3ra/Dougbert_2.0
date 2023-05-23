from twttr_functions import twttr_handler
from openAI import create_new_tweet, create_tweet_response
import random
import json

def post_tweet():
    # Load topics from json file
    with open('src/new_engagement/topics.json', 'r') as f:
        topics = json.load(f)['topics']

    # Choose between creating a new tweet or responding to a tweet
    new_tweet_probability = 0.0  # Probability of writing a new tweet
    rand_num = random.random()  # Generate a random number between 0 and 1

    try:
        if rand_num < new_tweet_probability:
            # This branch will be taken 5% of the time
            filtered_list = [topic for topic in topics if not topic['additional_context']]
            tweet = create_new_tweet.generate_tweet(filtered_list)
            twttr_handler.decide_action('tweet', tweet=tweet)
            print('Posted new tweet')
        else:
            # This branch will be taken 95% of the time
            tweet_id = twttr_handler.decide_action('random-timeline')
            tweet_conversation = twttr_handler.decide_action('conversation', tweet_id=tweet_id)
            tweet = create_tweet_response.build_message(tweet_conversation)
            twttr_handler.decide_action('tweet', tweet=tweet, tweet_id=tweet_id)
            print('Replied to tweet')
    except Exception as e:
        raise e

if __name__ == '__main__':
    post_tweet()