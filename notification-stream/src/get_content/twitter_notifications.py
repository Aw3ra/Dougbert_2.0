import snscrape.modules.twitter as sntwitter
import time
from datetime import timedelta, datetime
import asyncio
from prisma import Client
import tweepy
import os

LIKE_WEIGHT = 0.5
RETWEET_WEIGHT = 1
REPLY_WEIGHT = 13.5
QUOTE_WEIGHT = 1

# Set your Twitter API credentials
TWITTER_CONSUMER_KEY="qcajsxE6IsFaCxmH7ZkY9bndT"
TWITTER_CONSUMER_SECRET="7iAtLyT4zpDBQHAKJggkF3o9cBbQwURLq1HbyHEQAqGd53Szi8"
TWITTER_ACCESS_TOKEN="506661675-3kSqCEs2fSbSwso3FabS9OtLApfuUQuo5ja3KVG5"
  
TWITTER_ACCESS_TOKEN_SECRET="pp3RWMR1C5qwhKvgNg7g2q75MTCkPQMheRWMi8JzENFfw"

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

def get_search_notifications_query(twitter_handle, last_notification_timestamp):
    return f"to:{twitter_handle} OR @{twitter_handle} since:{last_notification_timestamp} -is:retweet -is:quote"

def calculate_engagement(tweet):
    return (
        tweet.likeCount * LIKE_WEIGHT
        + tweet.retweetCount * RETWEET_WEIGHT
        + tweet.replyCount * REPLY_WEIGHT
        + tweet.quoteCount * QUOTE_WEIGHT
    )

def get_media_urls(tweet):
    if tweet.media is not None:
        return [
            media.fullUrl if isinstance(media, sntwitter.Photo)
            else media.variants[0].url if isinstance(media, sntwitter.Gif)
            else None
            for media in tweet.media
        ]
    return []

def fetch_notifications(search_query, max_notifications=None, last_notification=None):
    notifications = []
    users = []
    count = 0
    print(f"Searching for notifications using the query: {search_query}")

    try:
        for tweet in enumerate(sntwitter.TwitterSearchScraper(search_query).get_items()):
            tweet = tweet[1]
            print(f"Tweet Created at: {tweet.date} | {last_notification}")
            if last_notification is not None and str(tweet.date) == last_notification:
                print("Last tweet ID found. Stopping the search.")
                break

            if max_notifications is not None and count >= max_notifications:
                break

            tweet_dict = {
                "tweetId": tweet.id,
                "content": tweet.rawContent,
                "created_at": tweet.date,
                "author_username": tweet.user.username,
                "author_id": tweet.user.id,
                "engagement": calculate_engagement(tweet),
                "media_urls": get_media_urls(tweet)
            }
            print(f"Found new notification from {tweet_dict['author_username']}")
            users.append(tweet.user)
            notifications.append(tweet_dict)
            count += 1
    except Exception as e:
        print(f"Error occurred while using sntwitter: {e}")
        print("Trying to fetch notifications using the Twitter API.")
        return 

    print(f"Found {len(notifications)} new notifications.")
    return notifications, users

async def save_notification(prisma_client, notification):
    try:
        if await prisma_client.notification.find_unique(where={"tweetId": str(notification["tweetId"])}):
            return
        media_urls = list(filter(None, notification["media_urls"]))

        await prisma_client.notification.create(
            {
                "tweetId": str(notification["tweetId"]),
                "content": notification["content"],
                "createdAt": notification["created_at"],
                "authorUsername": notification["author_username"],
                "authorId": str(notification["author_id"]),
                "engagement": notification["engagement"],
                "mediaUrls": media_urls,
            }
        )
    except Exception as e:
        print("Error saving notification to database: ", e)
        return

async def save_tweets_to_database(prisma_client, tweets):
    await asyncio.gather(*[save_notification(prisma_client, tweet) for tweet in tweets])

async def save_users_to_database(prisma_client, users):
    await asyncio.gather(*[save_friend(prisma_client, user) for user in users])

async def save_friend(prisma_client, user):
    try:
        if await prisma_client.friends.find_unique(where={"twitter_id": str(user.id)}) is not None:
            print(user.username, "already exists in the database. Updating the user.")
            await prisma_client.friends.update(where = {"twitter_id": str(user.id)}, data =
                {
                    "twitter_id": str(user.id),
                    "username": user.username,
                    "display_name": user.displayname,
                    "profile_image_url": user.profileImageUrl if user.profileImageUrl is not None else "",
                    "profile_banner_url": user.profileBannerUrl if user.profileBannerUrl is not None else "",
                    "profile_description": user.rawDescription if user.rawDescription is not None else "",
                    "followers": user.followersCount,
                    "verified": user.verified                    
                }
            )
            return
        await prisma_client.friends.create(
            {
                "twitter_id": str(user.id),
                "username": user.username,
                "display_name": user.displayname,
                "nicknames": [],
                "friendship_level": 50,
                "conversations": [],
                "following": False,
                "friendship_created_at": datetime.now(),
                "profile_image_url": user.profileImageUrl if user.profileImageUrl is not None else "",
                "profile_banner_url": user.profileBannerUrl if user.profileBannerUrl is not None else "",
                "profile_description": user.rawDescription if user.rawDescription is not None else "",
                "followers": user.followersCount,
                "verified": user.verified                    
            }
        )
        print(f"New friend {user.username}!")
    except Exception as e:
        print("Error saving user to database: ", e)
        return

async def pseudo_stream(twitter_handle, interval):
    prisma_client = Client()

    async def main():
        # Connect to the database
        await prisma_client.connect()

        # Check if there are any notifications in the database
        notification_count = await prisma_client.notification.count()

        if notification_count == 0:
            # If there are no notifications, fetch the 10 most recent notifications
            print("No notifications in the database. Fetching the 10 most recent notifications.")
            yesterday = datetime.utcnow() - timedelta(days=1)
            search_query = get_search_notifications_query(twitter_handle, yesterday.strftime('%Y-%m-%d'))
            recent_notifications = fetch_notifications(search_query, 10, prisma_client)

            # Save the recent notifications to the database
            await save_tweets_to_database(prisma_client, recent_notifications[0])

            # Save the new users to the database
            await save_users_to_database(prisma_client, recent_notifications[1])

        while True:
            # Get all notifications from the database
            notifications = await prisma_client.notification.find_many()

            # Sort the notifications by 'created_at' in descending order
            sorted_notifications = sorted(notifications, key=lambda n: n.createdAt, reverse=True)

            if sorted_notifications:
                last_notification = sorted_notifications[0]
                last_tweet_id = str(last_notification.createdAt)
                print("Last tweet ID: ", last_notification.authorUsername)
            else:
                last_tweet_id = None

            # Get new notifications since the last tweet ID
            yesterday = datetime.utcnow() - timedelta(days=1)
            search_query = get_search_notifications_query(twitter_handle, yesterday.strftime('%Y-%m-%d'))
            notifications = fetch_notifications(search_query, last_notification=last_tweet_id)

            # Save the new notifications to the database
            await save_tweets_to_database(prisma_client, notifications[0])

            # Save the new users to the database
            await save_users_to_database(prisma_client, notifications[1])

            # Wait for the specified interval before fetching new notifications
            time.sleep(interval)

    try:
        await main()
    except Exception as e:
        print("Error in main: ", e)
    finally:
        # Disconnect from the database
        await prisma_client.disconnect()

def run_twitter_notifications(twitter_handle, interval):
    asyncio.run(pseudo_stream(twitter_handle, interval))

if __name__ == "__main__":

    # Define the environment variables
    TWITTER_HANDLE = os.environ["TWITTER_HANDLE"]
    DATABASE_URL = os.environ["DATABASE_URL"]

    print("Starting Twitter Notifications for " + TWITTER_HANDLE)
    print("Using database " + DATABASE_URL)

    # Run the Twitter notifications
    run_twitter_notifications(TWITTER_HANDLE, 60)

