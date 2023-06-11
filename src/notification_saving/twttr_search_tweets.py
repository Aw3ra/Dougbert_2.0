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
        conn.request("GET", f"/search-users?query={query}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        tweets = data['globalObjects']['tweets']
        # dump it as a json
        notifications = []
        for tweet in tweets:
            if 'retweeted_status_id_str' in tweets[tweet] or tweets[tweet]['user_id'] == os.getenv("TWITTER_ID"):
                continue
            tweet_dict = {}
            tweet_dict['id'] = tweets[tweet]['id']
            tweet_dict['user_id'] = tweets[tweet]['user_id']
            # Convert to datetime object
            tweet_dict['created_at'] = datetime.strptime(tweets[tweet]['created_at'], '%a %b %d %H:%M:%S %z %Y')
            tweet_dict['full_text'] = tweets[tweet]['full_text']
            notifications.append(tweet_dict)
            # Return the notifications in reverse order
        return notifications[::-1]
    except Exception as e:
        raise e

def save_notifications(notifications):
    client = MongoClient(os.getenv("DATABASE_URL"))
    db = client["Shrempbrain_prod"]
    notifications_collection = db["notifications"]
    notifications_collection.insert_one
    try:
        if notifications is not None:
            saved_notifications = 0
            for notification in notifications:
                try:
                    result = notifications_collection.insert_one(
                        {
                            "_id": str(notification["id"]),
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
    session = os.getenv("SHREMPBRAIN_SESSION")
    twitter_handle = str(os.getenv("TWITTER_HANDLE"))
    max_retries = 5
    for i in range(max_retries):
        try:
            save_notifications(search_notifications(session, twitter_handle))
            break  # if the function runs successfully, break the loop
        except Exception as e:
            if i < max_retries - 1:  # i starts at 0, so we subtract 1
                print('Error encountered: ', str(e))
                print(f'Retrying after 5 seconds... (Attempt {i+2}/{max_retries})')  # i+2 because i starts at 0
                time.sleep(5)
            else:
                print('Error encountered on the final attempt. No further retries will be made.')
                raise  # re-raise the last exception

# if __name__ == '__main__':
#     search_notifications(session, twitter_handle)