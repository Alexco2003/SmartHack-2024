from typing import List
from utils.reader import *

class Graph:
    mapping_list: List[str] = []
    id_hashmap: dict[str, int] = {}
    adjacency_list: List[List[int]] = []

    @staticmethod
    def load_objects(objects):
        for object in objects:
            Graph.mapping_list.append(object.id)
            Graph.id_hashmap[object.id] = len(Graph.mapping_list) - 1

    @staticmethod
    def load_data():
        refineries = read_refineries("../data/refineries.csv")
        Graph.load_objects(refineries)

        tanks = read_tanks("../data/tanks.csv")
        Graph.load_objects(tanks)

        customers = read_customers("../data/customers.csv")
        Graph.load_objects(customers)

        for _ in Graph.mapping_list:
            Graph.adjacency_list.append([])

        connections = read_connections("../data/connections.csv")
        for connection in connections:
            Graph.adjacency_list[Graph.id_hashmap[connection['from_id']]].append(Graph.id_hashmap[connection['to_id']])



