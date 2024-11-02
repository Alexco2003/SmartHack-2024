from solver.astar import astar
from solver.graph import Graph
from solver.utils.types import Connection, Demand
from typing import List


class GameState:
    def __init__(self):
        self.graph = Graph()
        self.graph.load_data("../../data")
        self.demand_queue: List[Demand] = []
        self.connection_queue = []

    def update_refinery_current_stock(self, refinery_id: int, new_capacity: int):
        self.graph.refineries_dict[refinery_id].current_stock = new_capacity

    def get_refinery_current_stock(self, refinery_id: int):
        return self.graph.refineries_dict[refinery_id].current_stock

    def update_tank_current_stock(self, tank_id: int, new_capacity: int):
        self.graph.tanks_dict[tank_id].current_stock = new_capacity
    def get_tank_current_stock(self, tank_id: int):
        return self.graph.tanks_dict[tank_id].current_stock

    def update_refinery_production(self, refinery_id: int):
        if self.graph.refineries_dict[refinery_id].current_stock + self.graph.refineries_dict[refinery_id].production < self.graph.refineries_dict[refinery_id].capacity:
            self.graph.refineries_dict[refinery_id].current_stock += self.graph.refineries_dict[refinery_id].production
    def get_refinery_production(self, refinery_id: int):
        return self.graph.refineries_dict[refinery_id].production
    def update_connections(self):
        for connection in self.connection_queue[:]:
            connection[1] -= 1
            if connection[1] == 0:
                self.connection_queue.remove(connection)
                self.graph.connections_dict[(connection[0]['from_id'], connection[0]['to_id'])][0]['current_capacity'] = 0
    def add_connection_to_queue(self, connection, days, capacity):
        self.connection_queue.append([connection, days])
        self.graph.connections_dict[(connection['from_id'], connection['to_id'])][0]['current_capacity'] = capacity

    def get_connections(self):
        return self.connection_queue

    def successors(self, curr):
        L = []
        for neigh in self.graph.adjacency_list[curr]:
            connection = self.graph.connections_dict[(curr, neigh)]
            for conn in connection:
                if conn["current_capacity"] >= conn["max_capacity"]:
                    continue
                L.append(neigh)

        return L

    def load_demands(self, demands):
        self.demand_queue += demands
        self.demand_queue = sorted(self.demand_queue,
                                   key=lambda x: (x.start_delivery_day, x.end_delivery_day - x.start_delivery_day))

game = GameState()
print(game.successors(11))
# print(game.graph.id_hashmap['9ba06385-f553-4f2f-b4e7-f398373071a8'])
# print(astar(game.graph.id_hashmap['beb6ba68-6d89-48e0-a6aa-1ee978bafa27'], game.graph.id_hashmap['8a50c288-5063-433f-8da6-64f7a0b4f361'], 10000, lambda x,y: 1, game))