import requests
import json
import time



def post_tweet(tweet_text, session,key, in_reply_to_status_id=None):
    url = "https://twttrapi.p.rapidapi.com/create-tweet"
    try:
        tweets = []
        # If in_reply_to_status_id is not None, then the tweet is a reply to the tweet with the given ID.
        if len(tweet_text) > 280:
            tweets = split_text_by_punctuation(tweet_text)
        else:
            tweets.append(tweet_text)

        # Loop through the tweets and post them
        for tweet in tweets:
            if in_reply_to_status_id is not None:
                payload = {
                    "tweet_text": tweet,
                    "in_reply_to_tweet_id": in_reply_to_status_id
                }
            else:
                payload = {
                    "tweet_text": tweet,
                }
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'twttr-session': session,
                'X-RapidAPI-Key': key,
                'X-RapidAPI-Host': "twttrapi.p.rapidapi.com"
            }
            data = requests.post(url, data=payload, headers=headers).text
            try:
                data = json.loads(data)
                in_reply_to_status_id = data['data']['create_tweet']['tweet_result']['result']['rest_id']
                time.sleep(2)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        raise e

def split_text_by_punctuation(text, max_chars=280):
    split_text = []

    def closest_split(s, ch):
        index = max_chars
        while index > 0:
            if s[index] == ch:
                return index
            index -= 1
        return -1

    def split_chunk(chunk, split_char):
        while len(chunk) > max_chars:
            split_index = closest_split(chunk, split_char)
            if split_index == -1: 
                break
            split_text.append(chunk[:split_index+1].strip())
            chunk = chunk[split_index+1:].strip()
        return chunk

    # Step 1: Split by double new lines
    chunks = text.split('\n\n')

    for chunk in chunks:
        if len(chunk) > max_chars:
            # Step 2: Split by new lines if chunk is still too long
            chunk = split_chunk(chunk, '\n')

        if len(chunk) > max_chars:
            # Step 3: Split by full stops if line is still too long
            chunk = split_chunk(chunk, '.')

        if len(chunk) > max_chars:
            # Step 4: Split by spaces if sentence is still too long
            words = chunk.split(' ')
            new_sentence = ''
            for word in words:
                if len(new_sentence + ' ' + word) <= max_chars:
                    new_sentence += ' ' + word
                else:
                    split_text.append(new_sentence.strip())
                    new_sentence = word
            if new_sentence:
                split_text.append(new_sentence.strip())
        else:
            split_text.append(chunk)

    return split_text
