import networkx as nx
import sys
sys.path.append("../")
import Code.Nearest_Neighbour.nearest_neighbour_optimisation as nno

def test_nearest_neighbour_optimisation():
    # Create a sample graph
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3])
    G.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    
    # Define distances between nodes
    distances = {
        (0, 1): 1, (1, 0): 1,  # Adding both (0, 1) and (1, 0)
        (0, 2): 2, (2, 0): 2,  # Adding both (0, 2) and (2, 0)
        (0, 3): 3, (3, 0): 3,  # Adding both (0, 3) and (3, 0)
        (1, 2): 4, (2, 1): 4,  # Adding both (1, 2) and (2, 1)
        (1, 3): 5, (3, 1): 5,  # Adding both (1, 3) and (3, 1)
        (2, 3): 6, (3, 2): 6   # Adding both (2, 3) and (3, 2)
    }
    
    # Define the start node
    start_node = 0
    
    # Expected tour
    expected_tour = [0, 1, 2, 3]
    
    # Call the function
    tour = nno.nearest_neighbour_optimisation(G, start_node, distances)
    
    # Check if the tour matches the expected tour
    assert tour == expected_tour, f"Expected tour: {expected_tour}, Actual tour: {tour}"

# Run the test
test_nearest_neighbour_optimisation()