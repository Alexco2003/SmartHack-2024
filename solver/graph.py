from typing import List
from solver.utils.reader import *

class Graph:
    mapping_list: List[str] = []
    id_hashmap: dict[str, int] = {}
    adjacency_list: List[List[int]] = []

    refineries_dict: dict[int, Refinery] = {}
    tanks_dict: dict[int, Tank] = {}
    customers_dict: dict[int, Customer] = {}
    connections_dict: dict[(int, int), Connection] = {}

    @staticmethod
    def load_objects(objects):
        for object in objects:
            Graph.mapping_list.append(object.id)
            Graph.id_hashmap[object.id] = len(Graph.mapping_list) - 1

    @staticmethod
    def load_data(folder: str):
        refineries = read_refineries(folder + "/refineries.csv")
        Graph.load_objects(refineries)
        for refinery in refineries:
            Graph.refineries_dict[Graph.id_hashmap[refinery.id]] = refinery

        tanks = read_tanks(folder + "/tanks.csv")
        Graph.load_objects(tanks)
        for tank in tanks:
            Graph.tanks_dict[Graph.id_hashmap[tank.id]] = tank

        customers = read_customers(folder + "/customers.csv")
        Graph.load_objects(customers)
        for customer in customers:
            Graph.customers_dict[Graph.id_hashmap[customer.id]] = customer

        for _ in Graph.mapping_list:
            Graph.adjacency_list.append([])

        connections = read_connections(folder + "/connections.csv")
        for connection in connections:
            Graph.adjacency_list[Graph.id_hashmap[connection['from_id']]].append(Graph.id_hashmap[connection['to_id']])
            Graph.connections_dict[(Graph.id_hashmap[connection['from_id']], Graph.id_hashmap[connection['to_id']])] = connection


