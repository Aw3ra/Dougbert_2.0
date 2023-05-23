#!/usr/bin/env python3
from get_content.twitter_stream import start_streaming
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()


# Define the environment variables
TWITTER_HANDLE = os.getenv("TWITTER_HANDLE")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

print("Starting Twitter Notifications for " + TWITTER_HANDLE)

# Run the Twitter notifications using twitter api
start_streaming(TWITTER_BEARER_TOKEN, TWITTER_HANDLE)

# Run the Twitter notifications using snscraper instead of twitter api
# run_twitter_notifications(TWITTER_HANDLE, 60)