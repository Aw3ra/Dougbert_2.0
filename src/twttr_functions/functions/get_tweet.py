import http.client
import json
import time
import requests
import os



tweet_id = '1659703890265387008'

def get_tweet(tweet_id, key):
    conn = http.client.HTTPSConnection("twttrapi.p.rapidapi.com")
    headers = {
        'X-RapidAPI-Key': key,
        'X-RapidAPI-Host': "twttrapi.p.rapidapi.com"
    }
    conn.request("GET", f"/get-tweet?tweet_id={tweet_id}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    json_data = json.loads(data)
    return json_data['data']['tweet_result']['result']['legacy']['full_text']

def request_tweet(tweet_id, key):
    url = "https://twttrapi.p.rapidapi.com/get-tweet"
    querystring = {"tweet_id":tweet_id}
    headers = {
        'x-rapidapi-key': key,
        'x-rapidapi-host': "twttrapi.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response)
    return response.json()['data']['tweet_result']['result']['legacy']['full_text']

def get_tweet_conversation(tweet_id, key):
    try:
        url = "https://twttrapi.p.rapidapi.com/get-tweet"
        querystring = {"tweet_id":tweet_id}
        headers = {
            'x-rapidapi-key': key,
            'x-rapidapi-host': "twttrapi.p.rapidapi.com"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        user_name = response.json()['data']['tweet_result']['result']['core']['user_result']['result']['legacy']['screen_name']
        content = response.json()['data']['tweet_result']['result']['legacy']['full_text']
        conversation = [{'role': 'user', 'content': user_name + ': ' + content+'.'}]
        new_tweet_id = response.json()['data']['tweet_result']['result']['legacy'].get('in_reply_to_status_id_str', None)
        if new_tweet_id is not None:
            time.sleep(2)
            conversation += get_tweet_conversation(new_tweet_id, key) # Append the result of recursive call to conversation
        return conversation[::-1]
    except Exception as e:
        print('Error in get_tweet_conversation: '    + str(e), flush=True)
        print("Error with tweet_id: " + tweet_id, flush=True)
        raise e