import http.client

conn = http.client.HTTPSConnection("twttrapi.p.rapidapi.com")


def like_tweet(tweetID, session, key):
    payload = f"tweet_id={tweetID}"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'twttr-session': session,
        'X-RapidAPI-Key': key,
        'X-RapidAPI-Host': "twttrapi.p.rapidapi.com"
    }

    conn.request("POST", "/favorite-tweet", payload, headers)

    res = conn.getresponse()
    data = res.read()
    