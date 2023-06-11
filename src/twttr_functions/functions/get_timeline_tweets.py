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
        #  Filter out any entries that dont have a content section
        json_data = [i for i in json_data if 'content' in i]
        # Filter out any entries that dont have a clientEventInfo section in the content section
        json_data = [i for i in json_data if 'clientEventInfo' in i['content']]
        # Filter out any entries that dont have a component section in the clientEventInfo section of the content section
        json_data = [i for i in json_data if 'component' in i['content']['clientEventInfo']]
        # Filter out any entries that dont have a suggested_ranked_organic_tweet section in the component section of the clientEventInfo section of the content section
        json_data = [i for i in json_data if 'suggest_ranked_organic_tweet' in i['content']['clientEventInfo']['component']]

        # Pick random tweet
        json_data = random.choice(json_data)

        # Get the tweet id
        tweet_id = json_data['entryId'].split('-')[1]
        return tweet_id
    except Exception as e:
        print('Error encountered while getting a tweet from the timeline. Retrying...  '+ str(e), flush=True)


