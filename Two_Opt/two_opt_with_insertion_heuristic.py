import networkx as nx
import math
import matplotlib.pyplot as plt
import sys
from scipy.spatial import ConvexHull

import numpy as np
sys.path.append("../")


def plot_tour(G, tour):
    pos = {i: ([i][0], [i][1]) for i in G.nodes()}
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edges(G, pos, edgelist=tour, edge_color='r', width=2)
    plt.show()



def distance(point1, point2):
    return math.sqrt(((point1[0] - point2[0])**2) + ((point1[1] - point2[1])**2))

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # collinear
    return 1 if val > 0 else 2  # 1 for clockwise, 2 for counterclockwise

def convex_hull(points):
    n = len(points)
    if n < 3:
        return []

    hull = []
    l = min(points, key=lambda x: x[0])
    p = l
    q = None
    while True:
        hull.append(p)
        q = points[0]
        for i in range(1, n):
            if q == p or orientation(p, points[i], q) == 2:
                
                q = points[i]
        p = q
        if p == l:
            break

    return hull

def scipy_convex_hull(points):
    hull = ConvexHull(points)
    return [points[i] for i in hull.vertices]

def insertion_heuristic_convex_hull(points):
    path = scipy_convex_hull(points)
    print("Path", path)
    unvisited = set(points) - set(path)
    
    


    # print("Path", path)
    # print("Path Size", len(path))
    # print("\n\n")

    while unvisited:
        min_dist = float('inf')
        insert_point = None

        for candidate in unvisited:
            for i in range(len(path)):
                # Define edges
                prev_vertex = path[i - 1]
                edge1 = (prev_vertex, candidate)
                edge2 = (candidate, path[i])
                edge3 = (prev_vertex, path[i])
                
                # Calculate distances for edges
                edge1dist = distance(edge1[0], edge1[1])
                edge2dist = distance(edge2[0], edge2[1])
                edge3dist = distance(edge3[0], edge3[1])
                
                # Calculate the distance for the candidate insertion
                dist = (edge1dist + edge2dist) - edge3dist
                
                if dist < min_dist:
                    min_dist = dist
                    insert_point = (candidate, i)
        
        path.insert(insert_point[1], insert_point[0])
        unvisited.remove(insert_point[0])

    # print("Path Size After", len(path))
    return path

def get_insertion_heuristic_convex_hull_tour_edges(G, distances):
    coordinates = nx.spring_layout(G)
    points = [tuple(cord) for cord in coordinates.values()]
    initial_tour = insertion_heuristic_convex_hull(points)
    initial_tour_edges = []

    for point in initial_tour:
        new_point = tuple(point)
        for key, value in coordinates.items():
            new_value = tuple(value)
            if new_value == new_point:
                initial_tour_edges.append(key)
                break  # Found the corresponding key, no need to keep searching
    # print("Initial Tour Edges", initial_tour_edges)
    # print("Initial Tour Distance", two_opt_local_search_tour_edges_total_distance(two_opt_local_search_tour_edges(initial_tour_edges, G), distances))
    # print("\n\n")
    return initial_tour_edges

# This function finds a tour using the 2-opt local search heuristic.
def two_opt_local_search(G, distances, n):
    improved = True    
    tour = get_insertion_heuristic_convex_hull_tour_edges(G, distances)   
    # print("Tour", tour)

    while improved:
        improved = False
        for i in range(n):
            for j in range(i+1, n):
                currentEdge1 = (tour[i], tour[(i+1)])
                currentEdge2 = (tour[j], tour[(j+1)%n])
                    
                newEdge1 = (tour[i], tour[j])
                newEdge2 = (tour[(i+1)], tour[(j+1)%n])
                    
                currentEdgesDistance = distances[currentEdge1] + distances[currentEdge2]
                newEdgesDistance = distances[newEdge1] + distances[newEdge2]

                if newEdgesDistance < currentEdgesDistance:
                    tour[i+1:j+1] = tour[i+1:j+1][::-1]
                    improved = True
    # print("New Tour", tour) 
    # print("New Tour Distance", two_opt_local_search_tour_edges_total_distance(two_opt_local_search_tour_edges(tour, G), distances))
    return tour

    



def two_opt_local_search_tour_edges(tour, G):
    return [(tour[i-1], tour[i]) for i in range(G.number_of_nodes())]
                         


def two_opt_local_search_tour_edges_total_distance(tour_edges, distances):
    total_distance = 0
    for i, j in tour_edges:
        total_distance += distances[(i, j)]
    return total_distance   
        