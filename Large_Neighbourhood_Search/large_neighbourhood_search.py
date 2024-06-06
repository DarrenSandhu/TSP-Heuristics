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
				currentEdge1 = (tour[i], tour[(i+1)])
				# print("Current edge 1: "+ str(currentEdge1))
				currentEdge2 = (tour[j], tour[(j+1)%n])
				# print("Current edge 2: "+ str(currentEdge2))
                    
				newEdge1 = (tour[i], tour[j])
				newEdge2 = (tour[(i+1)], tour[(j+1)%n])
                    
				currentEdgesDistance = distances[currentEdge1] + distances[currentEdge2]
				# print("Current edge distance: "+ str(currentEdgesDistance))
				newEdgesDistance = distances[newEdge1] + distances[newEdge2]
				# print("New edge distance: "+ str(newEdgesDistance))

				if newEdgesDistance < currentEdgesDistance:
					tour[i+1:j+1] = tour[i+1:j+1][::-1]
					improved = True
				# print("\n")
	return tour


def lns_local_search_tour_edges(tour, G):
	return [(tour[i-1], tour[i]) for i in range(G.number_of_nodes())]
                         


def lns_local_search_tour_edges_total_distance(tour_edges, distances):
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

# Large Neighborhood Search Algorithm
def large_neighborhood_search(G, distances, n, max_iterations):
    tour = list(G.nodes())
	
    current_tour = two_opt_local_search(tour, distances, n)
    current_tour_edges = lns_local_search_tour_edges(current_tour, G)
    current_distance = lns_local_search_tour_edges_total_distance(current_tour_edges, distances)
	
    
    for iteration in range(max_iterations):
        # Perturbation: Perform random 2-opt swap on a portion of the tour
        perturbation_start = random.randint(0, len(current_tour) - 1)
        perturbation_end = random.randint(perturbation_start, len(current_tour) - 1)
        perturbed_tour = two_opt_swap(current_tour, perturbation_start, perturbation_end)

        # Local search: Perform 2-opt local search on the perturbed tour
        improved_tour = perturbed_tour
        improved_tour = two_opt_local_search(improved_tour, distances, n)
        improved_tour_edges = lns_local_search_tour_edges(improved_tour, G)

        # Acceptance criterion: Accept the improved tour if it has a shorter distance
        improved_distance = lns_local_search_tour_edges_total_distance(improved_tour_edges, distances)
        if improved_distance < current_distance:
            current_tour = improved_tour
            current_distance = improved_distance

    return current_tour


# n = 100
# G = nx.complete_graph(n)
# my_pos = {i: (random.random()*100, random.random()*100) for i in G.nodes()}

# start_time = time.time()

# distances = calculate_distances(G, my_pos)
# print(distances)
# test_edge = (0, 1)
# print("\n")
# print(distances[test_edge])
# large_neighborhood_search(G, distances, n, 100)

# # tour = two_opt_local_search(G, distances, n, my_pos)
# # tour_edges = two_opt_local_search_tour_edges(tour, G)
# # total_tour_distance = two_opt_local_search_tour_edges_total_distance(tour_edges, distances)

# end_time = time.time()