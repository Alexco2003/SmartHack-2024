from solver.graph import Graph

class GameState:
    def __init__(self, graph: Graph):
        self.graph = graph
        graph.load_data("../../data")
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
                self.graph.connections_dict[(connection[0]['from_id'], connection[0]['to_id'])]['current_capacity'] = 0
    def add_connection_to_queue(self, connection, days, capacity):
        self.connection_queue.append([connection, days])
        self.graph.connections_dict[(connection['from_id'], connection['to_id'])]['current_capacity'] = capacity

    def get_connections(self):
        return self.connection_queue







