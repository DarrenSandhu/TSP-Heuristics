import networkx as nx
import gurobipy as gp
import tsplib95 as tsp
import random
import matplotlib.pyplot as plt
from gurobipy import GRB, Model


problem = tsp.load('code/tsp/tsp_library/ulysses22.tsp')



# Create a graph without edges
G = nx.Graph()

# Add nodes with positions
for i, coords in problem.node_coords.items():
    G.add_node(i, pos=coords)

# Visualize the nodes using NetworkX

nx.draw(G, pos=nx.get_node_attributes(G, 'pos'), node_size=20, node_color='black')

plt.title("Nodes of the TSP Instance")
plt.show()


# # my_pos = {i: (random.random(), random.random()) for i in G.nodes()}

# print(G.edges(data=True))
# print()
# print(problem)
# print
# print(list(problem.get_edges()))

