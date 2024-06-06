import networkx as nx
import matplotlib.pyplot as plt
import math 
import sys
sys.path.append("../")

# Calculate the Euclidean distance between two points.
def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def plot_tour(G, tour, nodes):
    pos = {i: (nodes[i][0], nodes[i][1]) for i in G.nodes()}
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edges(G, pos, edgelist=tour, edge_color='r', width=2)
    plt.show()

# This function finds a tour using the nearest neighbour heuristic.
def nearest_neighbour(G, start_node, nodes):

    my_pos = {i: (nodes[i][0], nodes[i][1]) for i in G.nodes()}

    # Calculate the distance between each pair of nodes. and add it to the graph as an edge attribute.
    for i,j in G.edges():
        x1, y1 = my_pos[i]
        x2, y2 = my_pos[j]
        G[i][j]['weight'] = euclidean_distance(x1, y1, x2, y2)
    
    tour = [start_node]

    while len(tour) < G.number_of_nodes():
        i = tour[-1]
        min_length = min(G[i][j]['weight'] for j in G.neighbors(i) if j not in tour)
        nearest_node = [j for j in G.neighbors(i) if G[i][j]['weight'] == min_length and j not in tour][0]
        tour.append(nearest_node)
    
    return tour

def nearest_neighbour_tour_edges(tour, G):
    return [(tour[i-1], tour[i]) for i in range(G.number_of_nodes())]

def nearest_neighbour_tour_edges_total_distance(tour_edges, G):
    total_distance = 0
    for i, j in tour_edges:
        total_distance += G[i][j]['weight']
    return total_distance


def best_start_node(G, nodes):
    best_node = 0
    best_distance = 0
    for i in G.nodes():
        tour = nearest_neighbour(G, i, nodes)
        tour_edges = nearest_neighbour_tour_edges(tour, G)
        total_distance = 0
        for i, j in tour_edges:
            total_distance += G[i][j]['weight']
        if best_distance == 0 or total_distance < best_distance:
            best_distance = total_distance
            best_node = i
    return best_node


