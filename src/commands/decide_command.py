from openAI.functions import generate_text
import os
import json
api_key = os.getenv("OPENAI_API_KEY")
twitter_handle = str(os.getenv("TWITTER_HANDLE"))


from general_functions import find_json

prompts = find_json.find_json_file('command_generating_prompts.json')['command_decision']
LIST_OF_COMMANDS = [
"A: Do nothing",
"B: Reply to last tweet"
"C: Retweet last tweet",
"D: Like last tweet",
"E: Follow user",
"F: Search the internet",
"G: Check Solana price",
"H: Lookup user profile",
]

command_string = ""
for command in LIST_OF_COMMANDS:
    command_string += command + "\n"

# ---------------------------------------------------------------------------------#
# Function to decide which command to run based on the tweet
# Inputs:   tweet - an array of dictionaries in this format:
#                   {'role': 'user', 'content': 'Hello, my name is Doug'}
#                   {'role': 'assistant', 'content': 'Hello Doug, how are you doing today?'}
# Outputs:  the command to run
# ---------------------------------------------------------------------------------#
def decide_command(conversation):
    # Get the last two messages
    conversation = conversation[-1:]
    
    system_prompt = {"role": "system", "content": prompts["system_prompt"].replace("{COMMAND_LIST}", command_string).replace("{USER_NAME}", twitter_handle)}
    examples = [
        {"role": "user", "content": prompts["example_1"].replace("{USER_NAME}", twitter_handle)}, 
        {"role": "assistant", "content": prompts["answer_1"]}, 
        {"role": "user", "content": prompts["example_2"].replace("{USER_NAME}", twitter_handle)}, 
        {"role": "assistant", "content": prompts["answer_2"]}
        ]

    conversation.insert(0, system_prompt)
    for example in examples:
        conversation.insert(1, example)
    # -------------------------------------------------------------------------#
    # Get the text to generate
    # -------------------------------------------------------------------------#
    return generate_text.generate_text(api_key, prompt=conversation)