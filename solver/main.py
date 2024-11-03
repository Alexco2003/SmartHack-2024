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
print(refineries)

while i < 42:
    body = {"day": i, "movement": rounds[i]}
    round = Rest.play_round(start, body)

    print(round["totalKpis"])

    demands = round["demand"]
    print(demands)
    for demand in demands:

        cost_min = None
        solution = None
        for refinery in refineries:
            potential_solution = astar(game.graph.id_hashmap[refinery], game.graph.id_hashmap[demand["customerId"]], demand["amount"], lambda x, y: 1, game)
            if cost_min is None:
                solution = potential_solution
                cost_min = solution[0][1]
            elif cost_min < potential_solution[0][1]:
                solution = potential_solution
                cost_min = solution[0][1]

        move_round = demand["startDay"]
        for index, connection in enumerate(solution[0][3]):
            rounds[min(move_round, 39)].append({"connectionId": connection, "amount": demand["amount"]})
            move_round += solution[0][4][index]
    i+=1


Rest.end_session()