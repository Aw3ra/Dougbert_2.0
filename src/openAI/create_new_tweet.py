from .functions import generate_text
import os
import random
import json
from dotenv import load_dotenv






# Function to generate a new tweet based on some topics
def generate_tweet(topics):
    load_dotenv()
    with open('src/profile.json', 'r', encoding='utf-8') as f:
        examples = json.load(f)['system_prompts']['new_tweet']
        system_prompt = examples['system_prompt']
    api_key = os.getenv("OPENAI_API_KEY")
    message = []

    # pick random topic
    topic = random.choice(topics)
    exmaples = [
        {'role': 'user', 'content': examples['example_1']}, 
        {'role': 'assistant', 'content': examples['response_1']}, 
        {'role': 'user', 'content': examples['example_2']}, 
        {'role': 'assistant', 'content': examples['response_2']},
        ]

    message.append(system_prompt)
    for example in exmaples:
        message.append(example)
    request = {'role': 'user', 'content': "write a tweet about: " + topic['topic']}
    message.append(request)
    response = generate_text.generate_text(api_key, prompt=message)
    return response


if __name__ == '__main__':
    topics = [        {"topic": "How to brighten up your code with rainbow brackets", "additional_context": False},
        {"topic": "Why do programmers prefer dark mode", "additional_context": True},
        {"topic": "Exploring the world of tech-related animal GIFs", "additional_context": False}]
    print(generate_tweet(topics))