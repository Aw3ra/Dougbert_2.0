import datetime
from pymongo import MongoClient

import os
from dotenv import load_dotenv
import mysql.connector
load_dotenv()

db_config = {
  'user': os.getenv("USER"),
  'password': os.getenv("PASSWORD"),
  'host': os.getenv("HOST"),
  'database': os.getenv("DATABASE"),
  'ssl_ca': os.getenv("SSL_CERT"),
  'ssl_verify_cert': True,
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

def create_log(tweet_id, tweet_text, actions):

    if os.getenv("TWITTER_HANDLE").lower() == 'dougbertai':
        return
    # If actiones is an error
    actionString = ''
    print(actions)
    if isinstance(actions, Exception):
        actions = str(actions)
    else:
        # Convert each action item in the list from the letter to the action
        for action in actions:
            print(action)
            if action == 'A':
                actions = 'Ignore'
            elif action == 'B':
                actions = 'Reply'
            elif action == 'C':
                actions = 'Retweet'
            elif action == 'D':
                actions = 'Like'
            elif action == 'E':
                actions = 'Follow'
            elif action == 'F':
                actions = 'Reply with prior known info'
            elif action == 'G':
                actions = 'Check Solana price'
            elif action == 'H':
                actions = 'Lookup user profile'
            elif action == 'I':
                actions = 'Send tip'
            # If it is the first action, add it to the string
            if actionString == '':
                actionString = actions
            else:
                # Add action to the string  
                actionString += f', {actions}'
            


    timestamp = datetime.datetime.utcnow()
    tweetId = tweet_id
    tweetText = tweet_text
    actions = actionString

    # Upsert one log
    try:
        cursor.execute('INSERT INTO logs (timeStamp, tweetId, tweetText, actions) VALUES (%s, %s, %s, %s)',
               (timestamp, tweetId, tweetText, actions))
    # Commit your changes
        connection.commit()
    except Exception as e:
        print(f'Error in create_log: {e}')