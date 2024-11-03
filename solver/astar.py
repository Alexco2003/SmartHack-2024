from queue import PriorityQueue
from solver.utils.gameState import GameState


# A star algorithm which finds multiple paths until the quantity is reached
def astar(start, end, quantity, heuristic, state):
    frontier = PriorityQueue()
    frontier.put((0, start, [start], [], []))
    paths = []
    total_capacity = 0

    while not frontier.empty() and total_capacity < quantity:
        current_cost, current, path, conn_in_path, conn_times = frontier.get()

        # Check if we've reached the end node along this path
        if current == end:
            for conn in state.graph.connections_dict[(path[-2], path[-1])]:
                path_capacity = min(conn["max_capacity"],
                                    quantity - total_capacity)
                if path_capacity != 0:
                    paths.append((path, current_cost, path_capacity, conn_in_path, conn_times))
                    total_capacity += path_capacity

                    # ban_time = 0
                    # for index, connection in enumerate(conn_in_path):
                    #     ban_time += conn_times[index]
                    #     print("Am banat linia ", connection, " pentru ", conn_times[index], " zile")
                    #     state.add_connection_to_queue(state.graph.connections_hash[connection], ban_time, path_capacity)
                    #     print("x")
            return paths

        # Add all successors to the frontier if they lead towards a viable path
        for next_node in state.successors(current):
            for conn in state.graph.connections_dict[(current, next_node)]:
                if conn["current_capacity"] == 0:
                    new_cost = current_cost + conn["distance"]
                    priority = new_cost + heuristic(end, next_node)
                    frontier.put((priority, next_node, path + [next_node], conn_in_path + [conn["id"]], conn_times + [conn["lead_time_days"]]))

    return paths