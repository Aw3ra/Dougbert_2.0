import http.client
import json
import random

conn = http.client.HTTPSConnection("twttrapi.p.rapidapi.com")

tweet_id = '1657121978032050186'

def get_tweet(key, session):
    headers = {
        'twttr-session': session,
        'X-RapidAPI-Key': key,
        'X-RapidAPI-Host': "twttrapi.p.rapidapi.com"
    }
    conn.request("GET", "/following-timeline", headers=headers)

    res = conn.getresponse()
    data = res.read()

    json_data = json.loads(data)
    json_data = json_data['data']['timeline_response']['timeline']['instructions'][0]['entries']
    # filter out any entries that have their entry id that starts with anything except 'tweet'- these are not tweets
    json_data = [i for i in json_data if i['entryId'].startswith('tweet')]
    # Now of those tweets filter out any that are retweets
    json_data = [i for i in json_data 
             if 'legacy' in i['content']['content']['tweetResult']['result'] and 
                'RT' not in i['content']['content']['tweetResult']['result']['legacy'].get('full_text', '')]


    # Pick random tweet
    json_data = random.choice(json_data)

    # Get the tweet text
    text = json_data['content']['content']['tweetResult']['result']['legacy']['full_text']
    # Get the tweet id
    tweet_id = json_data['entryId'].split('-')[1]

    
    return tweet_id

if __name__ == '__main__':
    session = "H4sIAKpLZGQC/42RS3ObMBRGgx+4XsTDQIE4tlPz8iPJghESBmLjvyJA0hXTbDxkSf97je2ZetGZVistvnPud+e+NnnoB+kkyDN8bH6eGgq0EBxKAKirEmjNoDXnS50YG3UtyYtwrWGWb9ZAV4NN3p/xdfPrdC+ZuBh5OOhcSrbKkGqERsRUeB6ZMTJ7VjV2hGLtntIynfqOESp4jF4MJDtNRi7cPn1GpGbBSBnojj6KrKeVhOVMG6Z9+TEaOIqpDb/TpeiQbnDuJW9hkOSXBQwcetg7aX979vhNW12/86m+dXDPtGi8+LGI0xGuieDpATL+VZr9wdzmW+1h4UbYSIe9vqcnD84s2OaWijdTz4xYgKsPx3Iz1bTVurK7LgSvE4QnCel62DrTmTRrG6hWQnnZDx0SfAwmvn+NFJxCKYhoMStQy1Ep2ppx2QJhvJAlRVUo7rCQXDFKo4pV0TlMCtryAsk2CkXd7jjsSLmrUB1Ch8U+doP7y7IahBBMFozyEgpeXOR5niX4HHi9Adcha/pVahRqXknOQBYFSAZQ/fEm5FzI/d/oPvQyHCTH+B+Agz03P4aH20FvZR7PyKRQlMj3Z0H2TWKkQk/d7YM4/vx8bJr3998sQLDkyAIAAA=="
    key = "2665401a98mshb4ff8c9c9dc53efp1568abjsn0ce6e816b0c1"
    print(get_tweet(key, session))


