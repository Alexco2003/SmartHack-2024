import os

from dotenv import load_dotenv

from api_interface import Rest

# load all env variables
load_dotenv()

# set the API key
API_KEY = os.getenv("API_KEY")
Rest.set_api_key(API_KEY)
