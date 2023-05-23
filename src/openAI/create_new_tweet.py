from .functions import generate_text
import os
import random

api_key = os.getenv("OPENAI_API_KEY")
system_prompt = {'role': 'assistant', 'content': "Your name is DougbertAI. Your creator is @0xawera. you are to generate new tweets based on tweets or topics that are given to you. Make them funny and easy to understand, especially if the topic or tweet is a complex concept."}

# Function to generate a new tweet based on some topics
def generate_tweet(topics):
    message = []

    # pick random topic
    topic = random.choice(topics)
    exmaples = [{'role': 'user', 'content': "write a tweet about: How fast solana is"}, {'role': 'assistant', 'content': "Solana's speed is out of this world! Currently handling significantly more than the network's average of 4K transactions per second, plans are in place to ramp up to 600,000 TPS with the help of validator client, Firedancer. And that's not all, the upcoming Token-22 and network's runtime optimizations are set to further boost performance. We're not just fast, we're Solana fast!"}, {'role': 'user', 'content': "write a tweet about: comparing the pros and cons of ethereum vs solana from a technical standpoint."}, {'role': 'assistant', 'content': "write a tweet about: " + "🔍Let's talk #Ethereum vs. #Solana from a technical standpoint. \nEthereum Pros:\n✅ Proven security and decentralization\n✅ Large developer community and ecosystem\n✅ Robust smart contracts platform\n\nEthereum Cons:\n❌ High gas fees and scalability issues\n❌ Slower transaction speed\n\nSolana Pros:\n✅ High-speed transaction processing (up to 600,000 TPS planned)\n✅ Lower transaction fees\n✅ Growing ecosystem\n\nSolana Cons:\n❌ Younger, less tested network\n❌ Smaller developer community (growing fast, though!)\n\nBoth have unique strengths, choose wisely! 💡"}]

    message.append(system_prompt)
    for example in exmaples:
        message.append(example)
    request = {'role': 'user', 'content': "write a tweet about: " + topic['topic']}
    message.append(request)
    response = generate_text.generate_text(api_key, prompt=message)
    return response


if __name__ == '__main__':
    topics = ["dogs", "saying gm instead of goodmorning", "how centralised solana is"]
    print(generate_tweet(topics))