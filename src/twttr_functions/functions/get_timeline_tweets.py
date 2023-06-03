import http.client
import json
import random



tweet_id = '1657121978032050186'

def get_tweet(key, session):
    conn = http.client.HTTPSConnection("twttrapi.p.rapidapi.com")
    try:
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
    except Exception as e:
        print('Error encountered while getting a tweet from the timeline. Retrying...  '+ str(e), flush=True)




