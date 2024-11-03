import json
import os

from dotenv import load_dotenv

from solver.api_interface import ResponseType
from solver.linalg.player import LingalgPlayer

# load all env variables
load_dotenv()

# set the API key
API_KEY = os.getenv("API_KEY")
LingalgPlayer.set_api_key(API_KEY)

response: ResponseType = LingalgPlayer.play()
print(json.dumps(response, indent=4))
