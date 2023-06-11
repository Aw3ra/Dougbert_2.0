import http.client
import json
import requests
import time

conn = http.client.HTTPSConnection("twttrapi.p.rapidapi.com")

tweet_id = '1657121978032050186'

def get_tweet(tweet_id, key):
    try:
        headers = {
            'X-RapidAPI-Key': key,
            'X-RapidAPI-Host': "twttrapi.p.rapidapi.com"
        }
        conn.request("GET", f"/get-tweet-conversation?tweet_id={tweet_id}", headers=headers)

        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data)
        if len(json_data) == 0: return []

        json_data = json_data['data']['timeline_response']['instructions']
        content = []
        count = 0
        conversation= []
        for i in json_data[0]['entries']:
            dict_to_add = {}
            count += 1
            try:
                content = i['content']['content']['tweetResult']['result']['legacy']['full_text']
                user_name = i['content']['content']['tweetResult']['result']['core']['user_result']['result']['legacy']['screen_name']
                if user_name == 'shrempbrain': dict_to_add['role'] = 'assistant'
                else: dict_to_add['role'] = 'user'
                dict_to_add['content'] = user_name + ': ' +content
                conversation.append(dict_to_add)
            except Exception as e:
                break

        return conversation
    except Exception as e:
        print(e)
        raise e

def request_tweet(tweet_id, key):
    url = "https://twttrapi.p.rapidapi.com/get-tweet-conversation"
    querystring = {"tweet_id":tweet_id}
    headers = {
        'x-rapidapi-key': key,
        'twttr-session': "H4sIAKpLZGQC/42RS3ObMBRGgx+4XsTDQIE4tlPz8iPJghESBmLjvyJA0hXTbDxkSf97je2ZetGZVistvnPud+e+NnnoB+kkyDN8bH6eGgq0EBxKAKirEmjNoDXnS50YG3UtyYtwrWGWb9ZAV4NN3p/xdfPrdC+ZuBh5OOhcSrbKkGqERsRUeB6ZMTJ7VjV2hGLtntIynfqOESp4jF4MJDtNRi7cPn1GpGbBSBnojj6KrKeVhOVMG6Z9+TEaOIqpDb/TpeiQbnDuJW9hkOSXBQwcetg7aX979vhNW12/86m+dXDPtGi8+LGI0xGuieDpATL+VZr9wdzmW+1h4UbYSIe9vqcnD84s2OaWijdTz4xYgKsPx3Iz1bTVurK7LgSvE4QnCel62DrTmTRrG6hWQnnZDx0SfAwmvn+NFJxCKYhoMStQy1Ep2ppx2QJhvJAlRVUo7rCQXDFKo4pV0TlMCtryAsk2CkXd7jjsSLmrUB1Ch8U+doP7y7IahBBMFozyEgpeXOR5niX4HHi9Adcha/pVahRqXknOQBYFSAZQ/fEm5FzI/d/oPvQyHCTH+B+Agz03P4aH20FvZR7PyKRQlMj3Z0H2TWKkQk/d7YM4/vx8bJr3998sQLDkyAIAAA==",
        'x-rapidapi-host': "twttrapi.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring).text.split('{"data":{"timeline_response":{"instructions":[{"__typename":"TimelineAddEntries","entries":')[1]
    entries = response.split('{"content":')
    for entry in entries:
        if 'full_text' not in entry: continue
        else:
            entry = entry.split('full_text')[1]
            print(entry)
            print()
    response = json.loads(response.text+'"}')
    content = []
    count = 0
    conversation= []
    for i in response['entries']:
        dict_to_add = {}
        count += 1
        content = i['content']['content']['tweetResult']['result']['legacy']['full_text']
        user_name = i['content']['content']['tweetResult']['result']['core']['user_result']['result']['legacy']['screen_name']
        if user_name == 'DougbertAI': dict_to_add['role'] = 'assistant'
        else: dict_to_add['role'] = 'user'
        dict_to_add['content'] = user_name + ': ' +content
        conversation.append(dict_to_add)
    return conversation
    

if __name__ == '__main__':
    for i in range(10):
        print(request_tweet(tweet_id, "2665401a98mshb4ff8c9c9dc53efp1568abjsn0ce6e816b0c1"))
        time.sleep(60)
