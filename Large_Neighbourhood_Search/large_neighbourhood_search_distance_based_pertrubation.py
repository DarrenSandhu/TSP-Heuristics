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

def split_tour_by_pertrubation(tour, perturbated_start, perturbated_end):
    perturbed_tour = tour[perturbated_start:perturbated_end]
    return perturbed_tour

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

def get_greatest_distance_split(tour, perturbated_percentage_of_tour, distances):
    greatest_distance = 0
    perturbated_start = 0
    perturbated_end = 0

    for i in range(len(tour)):
        current_pertrubated_start = i
        current_pertrubated_end = int((i + (len(tour) * perturbated_percentage_of_tour)) % len(tour))
        # print("Tour Length: " + str(len(tour)))
        # print("Perturbated start: " + str(pertrubated_start))
        # print("Perturbated end: " + str(pertrubated_end))

        # Calculate the distance between the current pair of nodes
        if current_pertrubated_start < current_pertrubated_end:
            current_distance = sum(distances[(tour[(j-1) % len(tour)], tour[j])] for j in range(current_pertrubated_start, len(tour))) + sum(distances[(tour[j-1], tour[j])] for j in range(0, current_pertrubated_end))
        else:
            current_distance = sum(distances[(tour[(j-1) % len(tour)], tour[j])] for j in range(current_pertrubated_start, current_pertrubated_end)) 
        # print("Current distance: " + str(current_distance))
          
        # Update the greatest_distance and perturbation indices if the current_distance is greater
        if current_distance > greatest_distance:
            greatest_distance = current_distance
            perturbated_start = i
            perturbated_end = current_pertrubated_end
        
        # print("\n")

    # print("Greatest distance: " + str(greatest_distance))   
    return perturbated_start, perturbated_end, greatest_distance

          
          
        
    
# Large Neighborhood Search Algorithm
def large_neighborhood_search_using_distance_based_perturbation(G, distances, n, max_iterations):
    tour = list(G.nodes())
	
    current_tour = two_opt_local_search(tour, distances, n)	
    current_tour_edges = lns_local_search_tour_edges(current_tour, G)
    current_distance = lns_local_search_tour_edges_total_distance(current_tour_edges, distances)
	
    initial_current_tour = current_tour
	
    initial_current_distance = current_distance
	
    perturbated_percentage_of_tour = 0.3
    
    for iteration in range(max_iterations):
        # Perturbation: Perform distance based 2-opt swap on 30% of the tour
        # perturbated_start, perturbated_end, perturbated_distance = get_greatest_distance_split(current_tour, perturbated_percentage_of_tour, distances)
        perturbated_start = random.randint(0, len(current_tour) - 1)
        perturbated_end = random.randint(perturbated_start, len(current_tour) - 1)
        perturbated_distance = sum(distances[(current_tour[(j-1) % len(current_tour)], current_tour[j])] for j in range(perturbated_start, perturbated_end))
        print("Perturbated start: " + str(perturbated_start))
        print("Perturbated end: " + str(perturbated_end))
        print("Current tour: " + str(current_tour))
        perturbed_tour = split_tour_by_pertrubation(current_tour, perturbated_start, perturbated_end)
        print("Perturbated tour: " + str(perturbed_tour))
        # print("Perturbated distance: " + str(perturbated_distance))
        # Local search: Perform 2-opt local search on the perturbed tour
        improved_tour = perturbed_tour[1: len(perturbed_tour) - 1]
        print("Improved tour: " + str(improved_tour))
        improved_tour = [perturbed_tour[0]] + two_opt_local_search(improved_tour, distances, len(improved_tour)) + [perturbed_tour[len(perturbed_tour) - 1]]
        print("Two Opt Improved tour: " + str(improved_tour))
        # print("Improved tour: " + str(improved_tour))
        improved_G = nx.complete_graph(len(improved_tour))
        improved_tour_edges = lns_local_search_tour_edges(improved_tour, improved_G)
        # Acceptance criterion: Accept the improved tour if it has a shorter distance
        improved_distance = lns_local_search_tour_edges_total_distance(improved_tour_edges, distances)
        print("Perturbated distance: " + str(perturbated_distance))

        print("Improved distance: " + str(improved_distance))
        print("\n")
        # if improved_distance < perturbated_distance:
        #     adjusted_tour = current_tour[:perturbated_start] + improved_tour + current_tour[perturbated_end:]
        #     adjusted_tour_edges = lns_local_search_tour_edges(adjusted_tour, G)
        #     adjusted_distance = lns_local_search_tour_edges_total_distance(adjusted_tour_edges, distances)
        #     if adjusted_distance < current_distance:
        #         print("Current Distance: " + str(current_distance))
        #         print("Adjusted distance: " + str(adjusted_distance))
        #         current_tour = adjusted_tour
        #         current_distance = adjusted_distance

    # print("Initial tour:", str(initial_current_tour))
    # print("Initial distance:", str(initial_current_distance))
	
    # print("\n")
	
    # print("Final tour:", str(current_tour))
    # print("Final distance:", str(current_distance))
	
    return current_tour



n = 100
G = nx.complete_graph(n)
my_pos = {i: (random.random()*100, random.random()*100) for i in G.nodes()}

start_time = time.time()

distances = calculate_distances(G, my_pos)
# print(distances)
test_edge = (0, 1)
print("\n")
# print(distances[test_edge])
tour = large_neighborhood_search_using_distance_based_perturbation(G, distances, n, 100)

# tour = two_opt_local_search(G, distances, n, my_pos)
# tour_edges = two_opt_local_search_tour_edges(tour, G)
# total_tour_distance = two_opt_local_search_tour_edges_total_distance(tour_edges, distances)

end_time = time.time()