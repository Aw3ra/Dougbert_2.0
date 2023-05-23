import prisma
import asyncio
from datetime import datetime

async def save_tweet(prisma_client, tweet):
    await prisma_client.connect()
    try:
        if await prisma_client.notification.find_unique(where={"tweetId": str(tweet.data['id'])}):
            return    
        await prisma_client.notification.create(
            {
                "tweetId": str(tweet.data['id']),
                "content": str(tweet.data['text']),
                "createdAt": datetime.utcnow(),
                "authorUsername": 'None',
                "authorId": str(tweet.data['author_id']),
                "engagement": 0.0,
                "mediaUrls": [''],
            }
        )
    except Exception as e:
        print("Error saving tweet to database: ", e)
        return
    finally:
        await prisma_client.disconnect()

def run_save_tweet(prisma_client, tweet):
    asyncio.run(save_tweet(prisma_client, tweet))

