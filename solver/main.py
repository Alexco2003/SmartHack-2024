import os

from dotenv import load_dotenv

from api_interface import Rest

from solver.astar import astar
from solver.utils.gameState import GameState

# load all env variables
load_dotenv()

# set the API key
API_KEY = os.getenv("API_KEY")
Rest.set_api_key(API_KEY)

start = Rest.start_session()

rounds = [[] for _ in range(42)]

game = GameState("../data")

i = 0
refineries = game.graph.get_all_refineries_id()

while i < 42:
    body = {"day": i, "movement": rounds[i]}
    round = Rest.play_round(start, body)

    print(round["totalKpis"])

    demands = round["demand"]
    for demand in demands:
        cost_min = None
        solution = None
        for refinery in refineries:
            potential_solution = astar(refinery, demand["customerId"], demand["amount"], lambda x, y: 1, game)
            if cost_min is None:
                solution = potential_solution
                cost_min = solution[0][1]
            elif cost_min < potential_solution[0][1]:
                solution = potential_solution
                cost_min = solution[0][1]

        move_round = demand["startDay"]
        for connection in solution[0][3]:
            rounds[move_round].append({"connectionId": connection["id"], "amount": demand["amount"]})
            move_round += connection["lead_time_days"]


Rest.end_session()