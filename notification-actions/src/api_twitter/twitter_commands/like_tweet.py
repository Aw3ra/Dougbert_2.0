# Function to like a select tweet
# Inputs:  auth     - the authentication object
#          tweet_id - the id of the tweet to like
# Outputs: True     - the tweet was successfully liked
#          e        - any error that occurs
def like_tweet(auth, tweet_id):
    try:
        # Like the tweet using the client auth
        auth.like(tweet_id)
        return True
    except Exception as e:
        return Exception(f'Error: {str(e)}')
