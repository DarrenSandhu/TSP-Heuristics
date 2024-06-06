import networkx as nx
import sys
sys.path.append("../")
import Code.Nearest_Neighbour.nearest_neighbour as nn

def test_nearest_neighbour():
    # Create a sample graph
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3])
    G.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    
    # Define nodes with their coordinates
    nodes = {
        0: (0, 0),
        1: (1, 0),
        2: (0, 1),
        3: (1, 1)
    }
    
    # Define the start node
    start_node = 0
    
    # Expected tour
    expected_tour = [0, 1, 3, 2]
    
    # Call the function
    tour = nn.nearest_neighbour(G, start_node, nodes)
    
    # Check if the tour matches the expected tour
    assert tour == expected_tour, f"Failed with Expected tour: {expected_tour}, Actual tour: {tour}"

# Run the test
test_nearest_neighbour()