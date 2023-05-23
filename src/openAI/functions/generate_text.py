import openai
import os


# ---------------------------------------------------------------------------------#
# Get the json file for the OpenAI engines
# ---------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------#
# Function to generate text
# Inputs:   api_key - the OpenAI API key
#           prompt - the prompt to start the text generation
#           max_tokens - the maximum number of tokens to generate
#           engine - the engine to use for text generation
# Outputs:  the generated text
# ---------------------------------------------------------------------------------#
def generate_text(api_key, **kwargs):
    try:
        # -------------------------------------------------------------------------#
        # Set the default values for the kwargs
        # -------------------------------------------------------------------------#
        default_kwargs = {
                            'prompt': 'Say something witty', 
                            'max_tokens': 3000, 
                            'engine': 'gpt-3.5-turbo-0301',
                            'temp': 0.7
                        }
        default_kwargs.update(kwargs)
        kwargs = default_kwargs
        # -------------------------------------------------------------------------#
        # Set the OpenAI API key
        # -------------------------------------------------------------------------#
        openai.api_key = api_key
        # -------------------------------------------------------------------------#
        # Get the engine to use
        # -------------------------------------------------------------------------#
        # -------------------------------------------------------------------------#
        # Send the prompt to the AI
        # -------------------------------------------------------------------------#
        response = openai.ChatCompletion.create(
            model=kwargs['engine'],
            temperature=kwargs['temp'],
            messages=kwargs['prompt'],
            max_tokens=kwargs['max_tokens'],
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        # -------------------------------------------------------------------------#
        # Return the response
        # -------------------------------------------------------------------------#
        return response['choices'][0]['message']['content']
        # -------------------------------------------------------------------------#
    except Exception as e:
        return Exception(f'Error in generate_text: {e}')
# ---------------------------------------------------------------------------------#


if __name__ == '__main__':
    api_key  = os.getenv('OPENAI_API_KEY')
    print(api_key)
    messages = [{"role": "user", "content": "tell me about black holes"}]
    print(generate_text(api_key, prompt=messages))