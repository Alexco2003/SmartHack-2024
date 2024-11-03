from typing import List, Tuple, Callable
import heapq
#TODO: implementeaza verificari mai multe pentru succesori => sa nu depaseasca rafinariile capacitatea maxima, sa nu depaseasca tanks capacitatea maxima, sa nu fie folosite drumuri multiple etc
class Node:
    def __init__(self, node_id, g, h, parent=None, connection=None, capacity=0):
        self.node_id = node_id
        self.g = g                # Cost from start to this node
        self.h = h                # Heuristic cost to the end node
        self.parent = parent      # Parent node in the path
        self.connection = connection # Connection from Parent to Node (or None if Node is refinery)
        self.capacity = capacity

    @property
    def f(self):
        return self.g + self.h    # Total estimated cost

    def __lt__(self, other):
        return self.f < other.f

# quantity sent is min(customer.max_input, demand.capacity)
def astar(start_nodes: List[int], end_node: int, heuristic: Callable, quantity: int, game_state):
    open_list = []
    closed_set = set()

    for node in start_nodes:
        h = heuristic(node, end_node)
        start = Node(node, g=0, h=h)
        heapq.heappush(open_list, start)

    while open_list:
        current = heapq.heappop(open_list)

        if current.node_id == end_node:
            return reconstruct_path(current, game_state)

        closed_set.add(current)

        for connection in game_state.successors(current.node_id):
            neigh = game_state.graph.id_hashmap[connection["to_id"]]
            if neigh in closed_set:
                continue

            transfer_capacity = min(connection["max_capacity"] - connection["current_capacity"], quantity)
            g_cost = current.g + connection["distance"]

            h_cost = heuristic(neigh, end_node)
            neighbor = Node(neigh, g=g_cost, h=h_cost, parent=current, connection=connection, capacity=transfer_capacity)

            heapq.heappush(open_list, neighbor)

    return []


def reconstruct_path(current: Node, game_state) -> List[Tuple[int, int, int]]:
    path = []
    while current.parent is not None:
        path.append((current.node_id, current.capacity, current.connection["id"]))
        game_state.add_connection_to_queue(current.connection, current.connection["lead_time_days"], current.capacity)
        current = current.parent
    path.reverse()
    return path
