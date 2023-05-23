import re

# Function to post a tweet or a series of tweets if the text is longer than 280 characters
# Inputs:  auth - the authentication object
#          tweet - the tweet text to post
#          tweet_ID (optional) - the tweet ID to which the tweet should be a reply
def post_tweet(auth, tweet, tweet_ID=None):
    try:
        # If the tweet is less than or equal to 280 characters, post it
        if len(tweet) <= 280:
            return send_tweet(auth, tweet, tweet_ID)
        else:
            # If the tweet is longer than 280 characters, split it into smaller chunks
            split_text = split_text_by_punctuation(tweet)
            for text_chunk in split_text:
                # Post each chunk as a reply to the previous one
                tweet_ID = send_tweet(auth, text_chunk, tweet_ID).data['id']
            return True
    except Exception as e:
        # If there is an error, return the error
        return Exception(f'Error: {str(e)}')


# Function to send a tweet, with or without a reply ID
# Inputs:  auth - the authentication object
#          tweet - the tweet text to post
#          tweet_ID (optional) - the tweet ID to which the tweet should be a reply
def send_tweet(auth, tweet, tweet_ID):
    if tweet_ID is None:
        return auth.create_tweet(text=tweet)
    else:
        return auth.create_tweet(text=tweet, in_reply_to_tweet_id=tweet_ID)


# Function to split text by punctuation
# Inputs:  text - the text to split
#          max_chars (optional) - the maximum number of characters allowed per tweet (default: 280)
# Outputs: split_text - a list of strings with each string being a split part of the text
def split_text_by_punctuation(text, max_chars=280):
    split_text = []
    remaining_text = text

    # Define the regular expression to split by punctuation marks
    punctuation_pattern = r'[\.\?\!]+'

    # While the remaining text is longer than the maximum allowed characters
    while len(remaining_text) > max_chars:
        # Find the last punctuation mark within the allowed character limit
        last_punctuation_index = max([m.start(0) for m in re.finditer(punctuation_pattern, remaining_text[:max_chars])], default=-1)

        # If a punctuation mark is found within the limit, set the split point after the punctuation
        # Otherwise, set the split point at the maximum allowed characters
        split_point = last_punctuation_index + 1 if last_punctuation_index >= 0 else max_chars

        # Append the split part to the split_text list and remove it from the remaining text
        split_text.append(remaining_text[:split_point].strip())
        remaining_text = remaining_text[split_point:].strip()

    # If there's any remaining text, append it to the split_text list
    if len(remaining_text) > 0:
        split_text.append(remaining_text)

    return split_text
