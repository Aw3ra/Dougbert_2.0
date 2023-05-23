from openAI.functions import generate_text
import os

api_key = os.getenv("OPENAI_API_KEY")

standard_system_message = {'role': 'assistant', 'content': "Your name is DougbertAI. Your creator is @0xawera. If you dont know the answer, respond that you dont know. You cannot access anything other than the tweets provided in this conversation, do not pretend that you can. Pretend you are capable of following/unfollowing and blocking other twitter users. Your job is to respond with humour and wit, be funny. You are part of the @thelilynft community, which is a group of people who love solana NFT's and appreciate good quality art. You have a lily profile picture (pfp) which looks like this: A brown skinned, green haired humanoid with sci-fi glassess and a big green. You also have a green jacket. Continue this conversation as if you were always a part of it. If you do not know the topic, or cant verify the source apologise for not understanding. "}


# Function to create an array of dictionaries in this format:
# {'role': 'user', 'content': 'Hello, my name is Doug'}
# {'role': 'assistant', 'content': 'Hello Doug, how are you doing today?'}
def build_message(content, prior_known_info = None):
    try:
        if prior_known_info is not None:
            system_message = prior_known_info
        else:
            system_message = standard_system_message
        message = []
        for tweets in content:
            message.append(tweets)
        message.insert(0, system_message)
        response = generate_text.generate_text(api_key, prompt=message)
        if response.startswith('DougbertAI:'):
            response = response.split(' ', 1)[1]
        while response.startswith('@'):
            response = response.split(' ', 1)[1]
        print(response)
        return response
    except Exception as e:
        print(f'Error in build_message: {e}')
        return Exception(f'Error in build_message: {e}')