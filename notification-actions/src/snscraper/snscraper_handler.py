from .snscraper_functions import get_thread

# Function to decide which function to call
# Inputs:   action - the action to take, scrape or get thread
#           kwargs - the additional info required for the action
# Outputs:  None
def decide_action(action, **kwargs):
        # Call the appropriate function based on the action
        match action:
            case 'get_thread':
                return get_thread.get_tweet_by_id(kwargs['tweet_id'])
            case _:
                return 'Invalid action'
