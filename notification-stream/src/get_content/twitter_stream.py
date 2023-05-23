import tweepy
import random
from filelock import FileLock
from prisma import Client
import os
from save_content.save_to_prisma import run_save_tweet


prisma_lock = "prisma.lock"
prisma_client = Client()
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# TODO: Clean up code, add comments, add error handling
# ---------------------------------------------------------------------------------#
# Class to handle the stream
# Inputs:   tweepy.StreamingClient - the class to inherit from
# Outputs:  None
# Methods:  on_connect - function to do something on stream connect
#           on_disconnect - function to do something on stream disconnect
#           on_error - function to do something on stream error
#           add_written_rules - function to add rules to the stream from a json file
#           delete_written_rules - function to delete rules from the stream from a json file
#           on_tweet - function to do something on a tweet
class DBStreaming(tweepy.StreamingClient):
    # Function to do something on stream connect
    def on_connect(self):
        print("Stream connected")

    # Function to do something on stream disconnect
    # TODO: Add a way to reconnect if needed
    # TODO: maybe global variable for connection status
    # TODO: Post disconnect to database and/or discord instead of printing
    def on_disconnect(self):
        print("Stream disconnected")

    # Function to do something on stream error
    # TODO: Instead of returning false, add a way to reconnect
    # TODO: Post error to database and/or discord instead of printing
    def on_error(self, status_code):
        print("Stream error:", status_code)
        return False

    # Function to add rules to the stream from a json file
    def add_written_rules(self, TWITTER_HANDLE):
        rule = f"{TWITTER_HANDLE} -from:dougbertai -is:retweet"
        self.add_rules(tweepy.StreamRule(rule))

    # Function to delete all rules from the stream
    def delete_written_rules(self):
        rules = self.get_rules()
        if rules.data:
            for rule in rules.data:
                self.delete_rules(rule)
        else:
            print("No rules to delete")
    # Function to trigger when a tweet matches the streaming rules, check rules
    def on_tweet(self, tweet):
        with FileLock(prisma_lock):
            run_save_tweet(prisma_client, tweet)

        
# ---------------------------------------------------------------------------------#
# Function to start the twitter stream
# Input: token - Twitter bearer token
# Output: None
# ---------------------------------------------------------------------------------#
def start_streaming(token, twitter_handle):
    def start_stream(token):
        # Create a new instance of the IDPrinter class
        current_stream = DBStreaming(token)
        # Delete all rules from the stream
        current_stream.delete_written_rules()
        # Add rules to the stream
        current_stream.add_written_rules(twitter_handle)
        # Start the stream
        current_stream.filter(expansions='author_id', user_fields='username')
    # Start the stream
    start_stream(token)

if __name__ == "__main__":
    start_streaming(TWITTER_BEARER_TOKEN)


  