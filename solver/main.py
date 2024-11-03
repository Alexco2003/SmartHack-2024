import os
from typing import List

from dotenv import load_dotenv

from api_interface import Rest
from solver.api_interface import ResponseType
from solver.linalg.problem_definition import ProblemModel
from solver.utils.mapper import map_demand_type_to_demand
from solver.utils.types import Demand

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

demands: List[Demand] = map_demand_type_to_demand(response["demand"])
ProblemModel.load_data()
ProblemModel.load_demands(demands)
ProblemModel.process_data()

for index in range(len(ProblemModel.demands)):
    ProblemModel.process_demand(ProblemModel.demands[index])

moves = ProblemModel.moves
response_2: ResponseType = Rest.play_round(session_id, {"day": 1, "movements": moves})

print(response_2)
Rest.end_session()
