import time
import networkx as nx
import random
import matplotlib.pyplot as plt
import math 
import numpy as np
import re
import os

def two_opt_local_search(tour, distances, n):
    improved = True
    
    while improved:
        improved = False
        for i in range(n):
            for j in range(i+1, n):
                currentEdge1 = (tour[i], tour[(i+1) % n])
                currentEdge2 = (tour[j], tour[(j+1) % n])
                    
                newEdge1 = (tour[i], tour[j])
                newEdge2 = (tour[(i+1) % n], tour[(j+1) % n])
                    
                currentEdgesDistance = distances[currentEdge1] + distances[currentEdge2]
                newEdgesDistance = distances[newEdge1] + distances[newEdge2]

                if newEdgesDistance < currentEdgesDistance:
                    tour[i+1:j+1] = tour[i+1:j+1][::-1]
                    improved = True    
    
    return tour


def two_opt_local_search_tour_edges(tour, G):
    return [(tour[i-1], tour[i]) for i in range(G.number_of_nodes())]
                         


def two_opt_local_search_tour_edges_total_distance(tour_edges, distances):
    total_distance = 0
    for i, j in tour_edges:
        total_distance += distances[(i, j)]
    return total_distance   

def two_opt_swap(tour, i, j):
    new_tour = tour[:i]
    new_tour.extend(reversed(tour[i:j+1]))
    new_tour.extend(tour[j+1:])
    return new_tour

# Calculate the Euclidean distance between two points.
def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


# This function calculates the distances between each pair of nodes in the graph.
def calculate_distances(G, nodes):
    distances = {}
    for i, j in G.edges():
        x1, y1 = nodes[i]
        x2, y2 = nodes[j]
        distances[(i, j)] = euclidean_distance(x1, y1, x2, y2)
        distances[(j, i)] = distances[(i, j)]  # Include both directions for undirected graph
    return distances


def lns_local_search_tour_edges(tour, G):
	return [(tour[i-1], tour[i]) for i in range(G.number_of_nodes())]

# Large Neighborhood Search Algorithm With Convergence
def large_neighborhood_search_convergence(G, distances, n, max_iterations):
    tour = list(G.nodes())
    
    current_tour = two_opt_local_search(tour, distances, n)	
    current_tour_edges = two_opt_local_search_tour_edges(current_tour, G)
    current_distance = two_opt_local_search_tour_edges_total_distance(current_tour_edges, distances)
    
    iteration = 0

    while iteration < max_iterations:
        # Perturbation: Perform random 2-opt swap on a portion of the tour
        perturbation_start = random.randint(0, len(current_tour) - 1)
        perturbation_end = random.randint(perturbation_start, len(current_tour) - 1)
        perturbed_tour = two_opt_swap(current_tour, perturbation_start, perturbation_end)

        # Local search: Perform 2-opt local search on the perturbed tour
        improved_tour = perturbed_tour
        improved_tour = two_opt_local_search(improved_tour, distances, n)
        improved_tour_edges = two_opt_local_search_tour_edges(improved_tour, G)

        # Acceptance criterion: Accept the improved tour if it has a shorter distance
        improved_distance = two_opt_local_search_tour_edges_total_distance(improved_tour_edges, distances)
        if improved_distance < current_distance:
            current_tour = improved_tour
            current_distance = improved_distance
            iteration = 0
        else:
            iteration += 1

    return current_tour, current_distance


# n = 100
# G = nx.complete_graph(n)
# my_pos = {i: (random.random()*100, random.random()*100) for i in G.nodes()}
# print(my_pos)
# nx.draw(G, my_pos, with_labels=True)
# plt.show()
# distances = calculate_distances(G, my_pos)

# tour = list(G.nodes())
# tour_edges = two_opt_local_search_tour_edges(tour, G)
# tour_edges_total_distance = two_opt_local_search_tour_edges_total_distance(tour_edges, distances)

# current_tour = list(G.nodes())
# current_tour = two_opt_local_search(current_tour, distances, n)
# current_tour_edges = two_opt_local_search_tour_edges(current_tour, G)
# current_tour_edges_total_distance = two_opt_local_search_tour_edges_total_distance(current_tour_edges, distances)

# print("Tour Distance: " + str(tour_edges_total_distance))
# print("Tour Edges: " + str(tour_edges))
# print("Tour: " + str(tour))
# print("\n")
# print("Current Tour Distance: " + str(current_tour_edges_total_distance))
# print("Current Tour Edges: " + str(current_tour_edges))
# print("Current Tour: " + str(current_tour))

# # Plotting the graph for the previous tour
# plot_tour(G, tour, my_pos, "Previous Tour")
# plot_tour(G, current_tour, my_pos, "Current Tour")

# # print(inital)
# # print("\n")
# # print(current_tour)
# start_time = time.time()

# # print(distances)
# test_edge = (0, 10)
# print("\n")
# print(distances[test_edge])
# lns_convergence_tour, lns_convergence_distance = large_neighborhood_search_convergence(G, distances, n, 100)
# lns_tour, lns_distance = large_neighborhood_search(G, distances, n, 100)

# print("Convergence tour:", str(lns_convergence_tour))
# print("Convergence distance:", str(lns_convergence_distance))

# print("\n")

# print("Iteration Tour:", str(lns_tour))
# print("Iteration Distance:", str(lns_distance))

# plot_tour(G, lns_convergence_tour)
# plot_tour(G, lns_tour)