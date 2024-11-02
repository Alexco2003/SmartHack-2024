from solver.graph import Graph

class GameState:
    def __init__(self, graph: Graph):
        self.graph = graph
        graph.load_data()


