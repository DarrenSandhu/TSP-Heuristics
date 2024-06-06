import time
import networkx as nx
import random
import matplotlib.pyplot as plt
import math 
import numpy as np
import re
import os

import sys
sys.path.append("../")



def plot_tour(G, tour):
    pos = {i: ([i][0], [i][1]) for i in G.nodes()}
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edges(G, pos, edgelist=tour, edge_color='r', width=2)
    plt.show()

# This function finds a tour using the nearest neighbour heuristic.
def nearest_neighbour_optimisation(G, start_node, distances):
    tour = [start_node]

    while len(tour) < G.number_of_nodes():
        i = tour[-1]
        min_length = min(distances[(i, j)] for j in G.neighbors(i) if j not in tour)
        nearest_node = [j for j in G.neighbors(i) if distances[(i, j)] == min_length and j not in tour][0]
        tour.append(nearest_node)

    return tour

def nearest_neighbour_optimisation_tour_edges(tour, G):
    return [(tour[i-1], tour[i]) for i in range(G.number_of_nodes())]

def nearest_neighbour_tour_edges_total_distance(tour_edges, distances):
    total_distance = 0
    for i, j in tour_edges:
        total_distance += distances[(i, j)]
    return total_distance

def best_start_node(G, d):
    best_node = 0
    best_distance = 0
    for i in G.nodes():
        tour = nearest_neighbour_optimisation(G, i, d)
        tour_edges = nearest_neighbour_optimisation_tour_edges(tour, G)
        total_distance = 0
        for i, j in tour_edges:
            total_distance += G[i][j]['weight']
        if best_distance == 0 or total_distance < best_distance:
            best_distance = total_distance
            best_node = i
    return best_node


