from openAI.functions import generate_text
import os
import json
from dotenv import load_dotenv
import re
import random



# Function to create an array of dictionaries in this format:
# {'role': 'user', 'content': 'Hello, my name is Doug'}
# {'role': 'assistant', 'content': 'Hello Doug, how are you doing today?'}
def build_message(content, prior_known_info = None):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    with open('src/profile.json', 'r', encoding='utf-8') as f:
        examples = json.load(f)['system_prompts']['tweet_response']['system_prompts']
        # Randomly pick between the two system prompts
        system_prompt = random.choice(examples)

    standard_system_message = {'role': 'assistant', 'content': system_prompt}
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
        response = re.sub(r"^\w+:\s", "", response)
        return response
    except Exception as e:
        print(f'Error in build_message: {e}', flush=True)
        return Exception(f'Error in build_message: {e}')

if __name__ == '__main__':
    content = [{'role': 'user', 'content': 'Hello, my name is Doug'}]
    print(build_message(content))