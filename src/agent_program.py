from dotenv import load_dotenv, find_dotenv
import random
import os

load_dotenv(find_dotenv()) # load the .env file
user_agent_list = os.getenv('USER_AGENTS').split('\n') # get the user agents from the .env file and split them into a list

# function to return a next user agent from the list
def user_agent_switcher():

    if len(user_agent_list) == 0:
        raise Exception('No user agents found')

    index_number = random.randint(0, len(user_agent_list) - 1) # get a random index from the list
    
    while True:
        yield user_agent_list[index_number]
        index_number += 1
        if index_number == len(user_agent_list):
            index_number = 0



