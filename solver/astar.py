from queue import PriorityQueue


# A star algorithm which finds multiple paths until the quantity is reached
def astar(start, end, quantity, heuristic, state):
    frontier = PriorityQueue()
    frontier.put((0, start, [start]))
    paths = []
    total_capacity = 0

    while not frontier.empty() and total_capacity < quantity:
        current_cost, current, path = frontier.get()

        # Check if we've reached the end node along this path
        if current == end:
            for conn in state.graph.connections_dict[(path[-2], path[-1])]:
                path_capacity = min(conn["max_capacity"],
                                    quantity - total_capacity)
                paths.append((path, current_cost, path_capacity))
                total_capacity += path_capacity
            continue

        # Add all successors to the frontier if they lead towards a viable path
        for next_node in state.successors(current):
            for conn in state.graph.connections_dict[(current, next_node)]:
                new_cost = current_cost + conn["distance"]
                priority = new_cost + heuristic(end, next_node)
                frontier.put((priority, next_node, path + [next_node]))

    return paths