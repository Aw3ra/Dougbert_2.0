import http.client
import dotenv
import os
import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from datetime import datetime
import asyncio
import time

def search_notifications(session, query):
    conn = http.client.HTTPSConnection("twttrapi.p.rapidapi.com")
    rapid_api_key = os.getenv("RAPID_API_KEY")
    try:
        headers = {
            'twttr-session': session,
            'X-RapidAPI-Key': rapid_api_key,
            'X-RapidAPI-Host': "twttrapi.p.rapidapi.com"
        }
        query = f"/search-users?query={query}"
        conn.request("GET", query, headers=headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        tweets = data['globalObjects']['tweets']
        # If the tweet contains a "scope" key, filter these out
        tweets = {tweet: tweets[tweet] for tweet in tweets if 'scopes' not in tweets[tweet]}
        # dump it as a json
        new_notifications = []
        for tweet in tweets:
            if 'retweeted_status_id_str' in tweets[tweet] or tweets[tweet]['user_id'] == 1610746366682361856:
                continue
            tweet_dict = {}
            tweet_dict['id'] = tweets[tweet]['id']
            tweet_dict['user_id'] = tweets[tweet]['user_id']
            # Convert to datetime object
            tweet_dict['created_at'] = datetime.strptime(tweets[tweet]['created_at'], '%a %b %d %H:%M:%S %z %Y')
            tweet_dict['full_text'] = tweets[tweet]['full_text']
            new_notifications.append(tweet_dict)
            # Return the notifications in reverse order
        return new_notifications[::-1]
    except Exception as e:
        raise e

async def save_notifications(notifications):
    client = MongoClient(os.getenv("DATABASE_URL"))
    with open('src/profile.json', 'r', encoding='utf-8') as f:
        records = json.load(f)['config_data']
        database = records["Database_records"]['Database']
        collection = records["Database_records"]["Collection"]
    db = client[database]
    notifications_collection = db[collection]
    try:
        if notifications is not None:
            saved_notifications = 0
            for notification in notifications:
                try:
                    # Insert the notification into the database if it doesn't already exist based on the tweetId
                    if not notifications_collection.find_one({"tweetId": str(notification["id"])}):
                        result = notifications_collection.insert_one(
                            {
                                "tweetId": str(notification["id"]),
                                "content": notification["full_text"],
                                "createdAt": notification["created_at"],
                                "authorId": str(notification["user_id"]),
                                "actioned": False
                            }
                        )
                        if result:
                            saved_notifications += 1
                except DuplicateKeyError:
                    break
            print("Saved: ", saved_notifications)
    except Exception as e:
        raise e
    finally:
        client.close()

def get_notifications():
    dotenv.load_dotenv()
    session = os.getenv("SESSION")
    twitter_handle = str(os.getenv("TWITTER_HANDLE"))
    max_retries = 5
    for i in range(max_retries):
        try:
            asyncio.run(save_notifications(search_notifications(session, twitter_handle)))
            break  # if the function runs successfully, break the loop
        except Exception as e:
            if i < max_retries - 1:  # i starts at 0, so we subtract 1
                print('Error encountered: ', str(e))
                print(f'Retrying after 5 seconds... (Attempt {i+2}/{max_retries})')  # i+2 because i starts at 0
                time.sleep(5)
            else:
                print('Error encountered on the final attempt. No further retries will be made.')
                raise  # re-raise the last exception

if __name__ == '__main__':
    session = "blah"
    twitter_handle = "dougbertai"
    get_notifications()