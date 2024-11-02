import os
from typing import List

from dotenv import load_dotenv

from api_interface import Rest
from solver.api_interface import DemandType, ResponseType

# load all env variables
load_dotenv()

# set the API key
API_KEY = os.getenv("API_KEY")
Rest.set_api_key(API_KEY)

session_id = Rest.start_session()
response: ResponseType = Rest.play_round(
    session_id,
    {
        "day": 0,
        "movements": [],
    },
)

demands: List[DemandType] = response["demand"]
