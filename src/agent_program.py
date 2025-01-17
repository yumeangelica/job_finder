from dotenv import load_dotenv, find_dotenv
import random
import os

load_dotenv(find_dotenv())

# Get user agents from environment variable
user_agent_list = os.getenv('USER_AGENTS').split('\n')

def user_agent_switcher():
    """Generator function to switch between user agents"""
    if len(user_agent_list) == 0:
        raise Exception('No user agents found')

    while True:
        # Return a random user agent
        agent = random.choice(user_agent_list)
        print(f'User agent: {agent}')
        yield agent
