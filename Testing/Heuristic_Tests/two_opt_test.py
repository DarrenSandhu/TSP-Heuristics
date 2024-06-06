import networkx as nx
import sys
sys.path.append("../")
import Code.Two_Opt.two_opt_local_search as to
import Code.Two_Opt.two_opt_with_greedy_heuristic as togh
import Code.Two_Opt.two_opt_with_insertion_heuristic as toi
import Code.Two_Opt.two_opt_with_nearest_neighbour as tonn

def test_two_opt_local_search():
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
    
    # Define the number of nodes
    n = G.number_of_nodes()
    
    # Expected tour
    expected_tour = [0, 1, 2, 3]
    
    # Call the function
    tour = to.two_opt_local_search(G, distances, n)
    
    # Check if the tour matches the expected tour
    assert tour == expected_tour, f"Expected tour: {expected_tour}, Actual tour: {tour}"

def test_two_opt_with_greedy_heuristic():
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
    
    # Define the number of nodes
    n = G.number_of_nodes()
    
    # Expected tour
    expected_tour = [0, 1, 2, 3]
    
    # Call the function
    tour = togh.two_opt_local_search(G, distances, n)
    
    # Check if the tour matches the expected tour
    assert tour == expected_tour, f"Expected tour: {expected_tour}, Actual tour: {tour}"

def test_two_opt_with_insertion_heuristic():
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
    
    # Define the number of nodes
    n = G.number_of_nodes()
    
    # Expected tour
    expected_tour = [0, 2, 3, 1]
    
    # Call the function
    tour = toi.two_opt_local_search(G, distances, n)
    
    # Check if the tour matches the expected tour
    assert tour == expected_tour, f"Expected tour: {expected_tour}, Actual tour: {tour}"

def test_two_opt_with_nearest_neighbour_heuristic():
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
    
    # Define the number of nodes
    n = G.number_of_nodes()
    
    # Expected tour
    expected_tour = [0, 1, 2, 3]
    
    # Call the function
    tour = tonn.two_opt_local_search(G, distances, n)
    
    # Check if the tour matches the expected tour
    assert tour == expected_tour, f"Expected tour: {expected_tour}, Actual tour: {tour}"
# Run the test
test_two_opt_local_search()
test_two_opt_with_greedy_heuristic()
test_two_opt_with_nearest_neighbour_heuristic()
print("All tests passed")
test_two_opt_with_insertion_heuristic()
