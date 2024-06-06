def greedy_cycle_avoidance(G, distances):
    visited = set()
    tour = []
    current = 0
    visited.add(current)
    tour.append(current)
    while len(visited) < G.number_of_nodes():
        min_distance = float('inf')
        next_node = None
        for neighbor in G.neighbors(current):
            if neighbor not in visited and distances[(current, neighbor)] < min_distance:
                min_distance = distances[(current, neighbor)]
                next_node = neighbor
        visited.add(next_node)
        tour.append(next_node)
        current = next_node
        
    return tour
