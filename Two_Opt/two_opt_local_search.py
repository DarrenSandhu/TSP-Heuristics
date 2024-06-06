import networkx as nx
import matplotlib.pyplot as plt
import sys
sys.path.append("../")


def plot_tour(G, tour):
    pos = {i: ([i][0], [i][1]) for i in G.nodes()}
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edges(G, pos, edgelist=tour, edge_color='r', width=2)
    plt.show()
    

# This function finds a tour using the 2-opt local search heuristic.
def two_opt_local_search(G, distances, n):
	improved = True
	tour = list(G.nodes())

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
	return tour


def two_opt_local_search_tour_edges(tour, G):
	return [(tour[i-1], tour[i]) for i in range(G.number_of_nodes())]
                         


def two_opt_local_search_tour_edges_total_distance(tour_edges, distances):
	total_distance = 0
	for i, j in tour_edges:
		total_distance += distances[(i, j)]
	return total_distance   
        


