import os
from typing import List

from dotenv import load_dotenv

from api_interface import RequestBodyType, Rest
from solver.astar import astar
from solver.graph import Graph
from solver.utils.gameState import GameState
from solver.utils.types import Demand

# from solver.api_interface import ResponseType
# from solver.linalg.player import LingalgPlayer


# LingalgPlayer.set_api_key(API_KEY)

# response: ResponseType = LingalgPlayer.play()
# print(json.dumps(response, indent=4))


# Method to parse JSON data into a list of Demand objects
def parse_demand(data: List[dict]) -> List[Demand]:
    return [
        Demand(
            id=str(i),  # Assuming 'id' is not in JSON; using index as ID or you could generate UUIDs here
            customer_id=item["customerId"],
            quantity=item["amount"],
            post_day=item["postDay"],
            start_delivery_day=item["startDay"],
            end_delivery_day=item["endDay"],
        )
        for i, item in enumerate(data)
    ]


# load all env variables
load_dotenv()

# set the API key
API_KEY = os.getenv("API_KEY")
Rest.set_api_key(API_KEY)

start = Rest.start_session()

rounds = [[] for _ in range(42)]

game = GameState()

i = 0
refineries = game.graph.get_all_refineries_id()
tanks = game.graph.get_all_tanks_id()
# print(refineries)

start_refineries = [Graph.id_hashmap[x] for x in refineries]

demands = []

while i < 42:
    body: RequestBodyType = {"day": i, "movements": rounds[i]}
    round = Rest.play_round(start, body)

    print(round["totalKpis"])
    print(round["penalties"])

    d = parse_demand(round["demand"])
    game.load_demands(d)

    demands_copy = []
    movements = []

    for demand in game.demand_queue:
        customer_id = game.graph.id_hashmap[demand.customer_id]
        demand_capacity = min(game.graph.customers_dict[customer_id].max_input, demand.quantity)
        # presupunem ca trimitem tot
        demand.quantity -= demand_capacity
        while demand_capacity > 0:
            # print(customer_id, demand_capacity)
            path = astar(
                start_nodes=start_refineries,
                end_node=customer_id,
                quantity=demand_capacity,
                heuristic=lambda x, y: 1,
                game_state=game,
            )
            if not path:
                break
            for conn in path:
                rounds[i + 1].append(
                    {
                        "connectionId": conn[2],
                        "amount": conn[1],
                    }
                )
            sent_capacity = path[-1][1]
            demand_capacity -= sent_capacity

        if demand_capacity > 0 or demand.quantity > 0:
            # daca nu am reusit sa trimitem tot, updatam cantitatea ce trebuie trimisa
            if demand_capacity > 0:
                demand.quantity += demand_capacity
            demands_copy.append(demand)

    game.update_demands(demands_copy)
    # game.update_round()
    i += 1


Rest.end_session()
