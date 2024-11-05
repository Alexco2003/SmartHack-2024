from typing import List

from solver.astar import astar
from solver.graph import Graph
from solver.utils.types import Connection, Demand


class GameState:
    def __init__(self):
        self.graph = Graph()
        self.graph.load_data("../data")
        self.demand_queue: List[Demand] = []
        self.connection_queue = []

    def update_round(self):
        self.update_connections()
        self.update_refinery_production()

    def update_refinery_current_stock(self, refinery_id: int, new_capacity: int):
        self.graph.refineries_dict[refinery_id].current_stock = new_capacity

    def update_tank_current_stock(self, tank_id: int, new_capacity: int):
        self.graph.tanks_dict[tank_id].current_stock = new_capacity

    def update_refinery_production(self):
        for refinery in self.graph.refineries_dict.values():
            if refinery.current_stock + refinery.production < refinery.capacity:
                refinery.current_stock += refinery.production

    def update_connections(self):
        for blocked_connection_details in self.connection_queue[:]:
            # decrementing days
            blocked_connection_details[1] -= 1
            if blocked_connection_details[1] == 0:
                conn = blocked_connection_details[0]
                restored_capacity = blocked_connection_details[2]
                self.connection_queue.remove(blocked_connection_details)
                conn["current_capacity"] = min(0, conn["current_capacity"] - restored_capacity)

    def add_connection_to_queue(self, connection, days, capacity):
        self.connection_queue.append([connection, days, capacity])
        connection["current_capacity"] = max(connection["current_capacity"] + capacity, connection["max_capacity"])

    # returns a list with the valid connections from curr
    def successors(self, curr) -> List[Connection]:
        L = []
        for neigh in self.graph.adjacency_list[curr]:
            connection = self.graph.connections_dict[(curr, neigh)]
            for conn in connection:
                if self.is_valid_connection(conn):
                    L.append(conn)

        return L

    # check for overflow in refinary, tank
    # valideaza daca are suficient amount in stock ca sa poate fi trimisa comanda
    def is_valid_connection(self, connection):
        return connection["current_capacity"] < connection["max_capacity"]

    def load_demands(self, demands):
        self.demand_queue += demands
        # print(demands)
        self.demand_queue = sorted(
            self.demand_queue, key=lambda x: (x.start_delivery_day, x.end_delivery_day - x.start_delivery_day)
        )

    def update_demands(self, demands):
        self.demand_queue = demands


# TESTEAZA CA DACA APELEZI DE 2 ORI DIN ACEEASI SURSA SI DESTINATIE ITI DA CONEXIUNI DIFERITE
# game = GameState()
# start_nodes = [0,1,2,3,4,5,6,7,8]
# end_node = 221
# quantity = 500
# path = astar(start_nodes, end_node, lambda x,y: 1, quantity, game)
# print(path)
# path = astar(start_nodes, end_node, lambda x,y: 1, quantity, game)
# print(path)
# print(game.graph.id_hashmap['9ba06385-f553-4f2f-b4e7-f398373071a8'])
# print(astar(game.graph.id_hashmap['beb6ba68-6d89-48e0-a6aa-1ee978bafa27'], game.graph.id_hashmap['8a50c288-5063-433f-8da6-64f7a0b4f361'], 10000, lambda x,y: 1, game))
