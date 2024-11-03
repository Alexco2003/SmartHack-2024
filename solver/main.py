import os

from dotenv import load_dotenv

from api_interface import Rest, RequestBodyType

from solver.astar import astar
from solver.graph import Graph
from solver.utils.gameState import GameState

# from solver.api_interface import ResponseType
# from solver.linalg.player import LingalgPlayer


# LingalgPlayer.set_api_key(API_KEY)

# response: ResponseType = LingalgPlayer.play()
# print(json.dumps(response, indent=4))

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
tanks = game.graph.get_all_tanks_id()
print(refineries)

demands = []

while i < 42:
    body: RequestBodyType = {"day": i, "movements": rounds[i]}
    round = Rest.play_round(start, body)

    print(round["totalKpis"])
    print(round["penalties"])

    demands.extend(round["demand"])

    demands_copy = []

    # print(demands)
    for demand in demands:

        cost_min = None
        solution = None
        refinery_used = None

        for refinery in refineries:
            rf = game.graph.object_search(game.graph.id_hashmap[refinery])
            if rf.current_stock > 0:
                potential_solution = astar(
                    game.graph.id_hashmap[refinery],
                    game.graph.id_hashmap[demand["customerId"]],
                    min(demand["amount"], rf.current_stock),
                    lambda x, y: 1,
                    game,
                )
                if cost_min is None:
                    solution = potential_solution
                    cost_min = rf.capacity - rf.current_stock
                elif cost_min < rf.capacity - rf.current_stock:
                    solution = potential_solution
                    cost_min = rf.capacity - rf.current_stock

        if solution != None:
            move_round = demand["startDay"]
            for index, connection in enumerate(solution[0][3]):
                rounds[min(move_round, 39)].append({"connectionId": connection, "amount": solution[0][2]})
                move_round += solution[0][4][index]

            if demand["amount"] - solution[0][2] > 0:
                demands_copy.append(
                    {
                        "customerId": demand["customerId"],
                        "amount": demand["amount"] - solution[0][2],
                        "postDay": demand["postDay"],
                        "startDay": demand["startDay"],
                        "endDay": demand["endDay"],
                    }
                )
        else:
            demands_copy.append(demand)

    demands = demands_copy

    for refinery in refineries:

        if Graph.refineries_dict.get(Graph.id_hashmap[refinery]):
            Graph.refineries_dict[Graph.id_hashmap[refinery]].current_stock += Graph.refineries_dict[
                Graph.id_hashmap[refinery]
            ].production
        # game.update_refinery_production(game.graph.id_hashmap[refinery])

        ref = game.graph.object_search(game.graph.id_hashmap[refinery])

        # print(f"Refinery {ref.name} -> {ref.current_stock} -> {ref.capacity}")
        while ref.current_stock > ref.capacity:
            max_space = None
            tank_used = None
            # print("Hello Alex!")
            for tank in game.graph.adjacency_list[game.graph.id_hashmap[refinery]]:
                tk = game.graph.object_search(tank)
                # print(f"{tk.current_stock} -> {tk.capacity}")
                if max_space is None:
                    max_space = tk.capacity - tk.current_stock
                    # print(f"Start: {max_space}")
                    tank_used = tank
                elif max_space < tk.capacity - tk.current_stock:
                    max_space = tk.capacity - tk.current_stock
                    # print(f"Update: {max_space}")
                    tank_used = tank

            if max_space == 0:
                # print("rezervoare mereu pline")
                break
            ref.current_stock = max(0, ref.current_stock - max_space)
            rounds[i].append(
                {
                    "connectionId": game.graph.connections_dict[(game.graph.id_hashmap[ref.id], tank_used)],
                    "amount": max(0, ref.current_stock - max_space),
                }
            )
            # print({"connectionId": game.graph.connections_dict[(game.graph.id_hashmap[ref.id], tank_used)]["id"],"amount": max(0, ref.current_stock - max_space)})

    i += 1


Rest.end_session()
