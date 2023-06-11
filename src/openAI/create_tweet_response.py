from openAI.functions import generate_text
import os
import json
from dotenv import load_dotenv




# Function to create an array of dictionaries in this format:
# {'role': 'user', 'content': 'Hello, my name is Doug'}
# {'role': 'assistant', 'content': 'Hello Doug, how are you doing today?'}
def build_message(content, prior_known_info = None):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    with open('src/profile.json', 'r', encoding='utf-8') as f:
        examples = json.load(f)['system_prompts']['tweet_response']
        system_prompt = examples['system_prompt']

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
        if len(message) < 2:
            # Add two examples to the message
            message.append({'role': 'user', 'content': '0xAwera: Hello, my name is awera!'})
            message.append({'role': 'assistant', 'content': 'DougbertAI: Hello awera, how are you doing today?'})
            message.append({'role': 'user', 'content': '0xAwera: I am doing great, how are you?'})
            message.append({'role': 'assistant', 'content': 'DougbertAI: I am doing well, thank you for asking.'})
        response = generate_text.generate_text(api_key, prompt=message)
        if response.startswith('DougbertAI:'):
            response = response.split(' ', 1)[1]
        while response.startswith('@'):
            response = response.split(' ', 1)[1]
        return response
    except Exception as e:
        print(f'Error in build_message: {e}', flush=True)
        return Exception(f'Error in build_message: {e}')


def build_tip_message(content, prior_known_info = None):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    system_prompt = "You are DougbertAI and you have been tasked with sending a tip in response to tweets, your job is to write the message that accompanies the tip."

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
        if len(message) < 2:
            # Add two examples to the message
            message.append({'role': 'user', 'content': '0xAwera: Wow you are so nice!'})
            message.append({'role': 'assistant', 'content': 'DougbertAI: Thankyou so much for telling me that I am nice! I have sent you a tip!'})
            message.append({'role': 'user', 'content': '0xAwera: Wow you have such beautiful eyes!'})
            message.append({'role': 'assistant', 'content': 'DougbertAI: Thankyou so much for telling me that I have beautiful eyes! I have sent you a tip!'})
        response = generate_text.generate_text(api_key, prompt=message)
        if response.startswith('DougbertAI:'):
            response = response.split(' ', 1)[1]
        while response.startswith('@'):
            response = response.split(' ', 1)[1]
        return response
    except Exception as e:
        print(f'Error in build_message: {e}', flush=True)
        return Exception(f'Error in build_message: {e}')


if __name__ == '__main__':
    content = [{'role': 'user', 'content': 'Hello, my name is Doug'}]
    print(build_message(content))