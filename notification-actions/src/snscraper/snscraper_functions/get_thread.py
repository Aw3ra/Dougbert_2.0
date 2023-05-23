import snscrape.modules.twitter as sntwitter
import re

def get_tweet_by_id(tweet_id, thread=[]):
    scraper = sntwitter.TwitterTweetScraper(tweet_id)
    tweet = next(scraper.get_items(), None)

    if tweet:
        cleaned_content = re.sub(r'^(@[\w]+\s)+', '', tweet.rawContent).strip()
        thread.insert(0, f"{tweet.user.username}: {cleaned_content}")
        if tweet.inReplyToTweetId is not None:
            return get_tweet_by_id(tweet.inReplyToTweetId, thread)
    else:
        print("Tweet not found")
    return thread



if __name__ == "__main__":
    tweet_id = "1648793846833192966"  # Replace with the desired tweet ID
    thread = get_tweet_by_id(tweet_id)

    for tweet in thread:
        print(tweet)