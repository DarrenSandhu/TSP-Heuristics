import time
import networkx as nx
import matplotlib.pyplot as plt
import math 
import os
import sys
sys.path.append("../")

import Code.Helper_Methods.file_helper as file_helper
import Code.Helper_Methods.json_library_helper as json_helper

import Code.Nearest_Neighbour.nearest_neighbour as nn
import Code.Nearest_Neighbour.nearest_neighbour_optimisation as nno
import Code.Two_Opt.two_opt_local_search as two_opt
import Code.Two_Opt.two_opt_with_nearest_neighbour as two_opt_nn
import Code.Two_Opt.two_opt_with_greedy_heuristic as two_opt_gh
import Code.Two_Opt.two_opt_with_insertion_heuristic as two_opt_ih
import Code.Large_Neighbourhood_Search.large_neighbourhood_search as lns
import Code.Large_Neighbourhood_Search.large_neighbourhood_search_convergence as lns_conv
import Code.Miller_Tucker_Zemlin.mip_solver as mtz

############################################################################################################
######      These functions are used to read and get the lines from the tsp accuracy list file  ############
############################################################################################################

def read_file(file_name):
    with open(file_name) as f:
        lines = f.read().splitlines()
    return lines

def get_accuracy_list():
    tsp_optimal_solutions_file = 'tsp/tsplib_optimal_solutions/tsp_accuracy_list' 
    lines = read_file(tsp_optimal_solutions_file)
    accuracy_list = []
    for each_line in lines:
        # Get 3rd word
        words = each_line.split()
        name = words[0]
        accuracy = words[2]
        accuracy_list.append([name, accuracy])
    return accuracy_list

accuracy_list = get_accuracy_list()

############################################################################################################
###### These functions are used to calculate the Euclidean distance between two points and to calculate ####
######                  the distances between each pair of nodes in the graph.                        ######
############################################################################################################


# Calculate the Euclidean distance between two points.
def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# This function calculates the distances between each pair of nodes in the graph.
def calculate_distances(G, nodes, algortithm):
    distances = {}
    for i, j in G.edges():
        x1, y1 = nodes[i]
        x2, y2 = nodes[j]
        distances[(i, j)] = euclidean_distance(x1, y1, x2, y2)
        if (algortithm != "Nearest Neighbour"):
            distances[(j, i)] = distances[(i, j)]  # Include both directions for undirected graph
    return distances


############################################################################################################
###### These functions are used to get the tour data and the total distance of the tour for the given ######
######                       tsp file and algorithm.                                                  ######
############################################################################################################

# This function returns the node positions for the given file name.
def get_node_positions(file_name):
    file_lines = file_helper.read_file(file_name) # Read the file and get the lines
    (name,n,nodes,correct) = file_helper.get_instance(file_lines) # Get the instance from the file including the number of nodes and the nodes
    my_pos = {i: (nodes[i][0], nodes[i][1]) for i in range(n)} # Get the position of the nodes
    return my_pos

# This function returns the total distance of the tour given the file name and the algorithm.
def single_tsplib_file_tour_data(file_name, algorithm):
    file_lines = file_helper.read_file(file_name) # Read the file and get the lines
    (name,n,nodes,correct) = file_helper.get_instance(file_lines) # Get the instance from the file including the number of nodes and the nodes

    # Check if the file is correct format
    if correct:

        G = nx.complete_graph(n) # Create a complete graph with n nodes

        # Check if algorithm is nearest neighbour and perform the nearest neighbour search to find the tour
        if algorithm == "Nearest Neighbour":
            tour = nn.nearest_neighbour(G, 1, nodes) # Get the tour using the nearest neighbour algorithm

            tour_edges = nn.nearest_neighbour_tour_edges(tour, G) # Get the tour edges

            return tuple([tour_edges, G, n, tour, nodes]) # Return the tour edges, the graph, and the number of nodes
        
        # Check if algorithm is nearest neighbour optimisation and perform the nearest neighbour optimisation search to find the tour
        elif algorithm == "Nearest Neighbour Optimisation":
            my_pos = {i: (nodes[i][0], nodes[i][1]) for i in G.nodes()} # Get the position of the nodes
            distances = calculate_distances(G, my_pos, algorithm) # Calculate the distances between the nodes

            tour = nno.nearest_neighbour_optimisation(G, 1, distances) # Get the tour using the nearest neighbour optimisation algorithm
     
            tour_edges = nno.nearest_neighbour_optimisation_tour_edges(tour, G) # Get the tour edges

            return tuple([tour_edges, G, n, distances, my_pos, tour]) # Return the tour edges, the graph, the number of nodes, the distances, and the position of the nodes
        
        # Check if algorithm is large neighbourhood search and perform the large neighbourhood search to find the tour
        elif algorithm == "Large Neighbourhood Search":
            my_pos = {i: (nodes[i][0], nodes[i][1]) for i in G.nodes()} # Get the position of the nodes
            distances = calculate_distances(G, my_pos, algorithm) # Calculate the distances between the nodes

            tour = lns.large_neighborhood_search(G, distances, n, 100) # Get the tour using the large neighbourhood search algorithm

            tour_edges = lns.lns_local_search_tour_edges(tour, G) # Get the tour edges

            return tuple([tour_edges, G, n, distances, my_pos, tour]) # Return the tour edges, the graph, the number of nodes, the distances, the position of the nodes, and the tour
        
        # Check if algorithm is large neighbourhood search convergence and perform the large neighbourhood search convergence to find the tour
        elif algorithm == "Large Neighbourhood Search Convergence":
            my_pos = {i: (nodes[i][0], nodes[i][1]) for i in G.nodes()} # Get the position of the nodes
            distances = calculate_distances(G, my_pos, algorithm) # Calculate the distances between the nodes

            tour, lns_conv_total_distance = lns_conv.large_neighborhood_search_convergence(G, distances, n, 10000) # Get the tour using the large neighbourhood search convergence 0algorithm with the set number of loops being 10000, and also getting the total distance of the tour

            tour_edges = lns_conv.lns_local_search_tour_edges(tour, G) # Get the tour edges

            return tuple([tour_edges, G, n, distances, my_pos, tour, lns_conv_total_distance]) # Return the tour edges, the graph, the number of nodes, the distances, the position of the nodes, the tour, and the total distance of the tour
        
        # Check if algorithm is two opt and perform the two opt to find the tour
        elif algorithm == "Two Opt":
            my_pos = {i: (nodes[i][0], nodes[i][1]) for i in G.nodes()} # Get the position of the nodes
            distances = calculate_distances(G, my_pos, algorithm) # Calculate the distances between the nodes

            tour = two_opt.two_opt_local_search(G, distances, n) # Get the tour using the two opt algorithm

            tour_edges = two_opt.two_opt_local_search_tour_edges(tour, G) # Get the tour edges

            return tuple([tour_edges, G, n, distances, my_pos, tour]) # Return the tour edges, the graph, the number of nodes, the distances, and the position of the nodes

        # Check if algorithm is two opt and perform the two opt with nearest neighbour to find the tour
        elif algorithm == "Two Opt with Nearest Neighbour":
            my_pos = {i: (nodes[i][0], nodes[i][1]) for i in G.nodes()} # Get the position of the nodes
            distances = calculate_distances(G, my_pos, algorithm) # Calculate the distances between the nodes

            tour = two_opt_nn.two_opt_local_search(G, distances, n) # Get the tour using the two opt algorithm

            tour_edges = two_opt_nn.two_opt_local_search_tour_edges(tour, G) # Get the tour edges

            return tuple([tour_edges, G, n, distances, my_pos, tour]) # Return the tour edges, the graph, the number of nodes, the distances, and the position of the nodes
        
        # Check if algorithm is two opt and perform the two opt with greedy heuristic to find the tour
        elif algorithm == "Two Opt with Greedy Heuristic":
            my_pos = {i: (nodes[i][0], nodes[i][1]) for i in G.nodes()} # Get the position of the nodes
            distances = calculate_distances(G, my_pos, algorithm) # Calculate the distances between the nodes

            tour = two_opt_gh.two_opt_local_search(G, distances, n) # Get the tour using the two opt algorithm

            tour_edges = two_opt_gh.two_opt_local_search_tour_edges(tour, G) # Get the tour edges

            return tuple([tour_edges, G, n, distances, my_pos, tour]) # Return the tour edges, the graph, the number of nodes, the distances, and the position of the nodes
        
        # Check if algorithm is two opt and perform the two opt with insertion heuristic to find the tour
        elif algorithm == "Two Opt with Insertion Heuristic":
            my_pos = {i: (nodes[i][0], nodes[i][1]) for i in G.nodes()} # Get the position of the nodes
            distances = calculate_distances(G, my_pos, algorithm) # Calculate the distances between the nodes

            tour = two_opt_ih.two_opt_local_search(G, distances, n) # Get the tour using the two opt algorithm

            tour_edges = two_opt_ih.two_opt_local_search_tour_edges(tour, G) # Get the tour edges

            return tuple([tour_edges, G, n, distances, my_pos, tour]) # Return the tour edges, the graph, the number of nodes, the distances, and the position of the nodes
        
        # If algorithm not recognised, return None
        else:
            return None


    # If the file is not correct format, return None
    else:
        return None
    

# This function returns the total distance of the tour given the correct file name and the algorithm.
def single_tsp_file_tour_edges_total_distance(file_name, algorithm):
    print("Calculating the time taken to find the distance of the " + algorithm + " tour for the tsp file...")

    tsp_file_edges = single_tsplib_file_tour_data(file_name, algorithm) # Get the tour edges for the file using the given algorithm
    total_distance = 0 # Initialise the total distance of the tour to 0

    # Check if algorithm is Large Neighbourhood Search Convergence and return the total distance of the tour which is the 7th element in the tuple
    if algorithm == "Large Neighbourhood Search Convergence":
        total_distance = tsp_file_edges[6]
    
    # Check if algorithm is two opt with insertion heuristic and return the total distance of the tour
    elif algorithm == "Two Opt with Insertion Heuristic":
        total_distance = two_opt_ih.two_opt_local_search_tour_edges_total_distance(tsp_file_edges[0], tsp_file_edges[3]) # Get the total distance of the tour
        

    # Check if algorithm is not Nearest Neighbour and return the total distance of the tour
    elif algorithm != "Nearest Neighbour":
        tour_edge = tsp_file_edges[0]
        for i, j in tour_edge:
            G = tsp_file_edges[1]
            total_distance += tsp_file_edges[3][(i, j)] 

    # Check if algorithm is Nearest Neighbour and return the total distance of the tour
    elif algorithm == "Nearest Neighbour":
        tour_edge = tsp_file_edges[0]
        for i, j in tour_edge:
            G = tsp_file_edges[1]
            total_distance += G[i][j]['weight']
    
    # Get the name of the file removing the path and file type
    name = file_name.split("/")[-1].replace(".tsp", "")

    # Check if the file is in the accuracy list
    accuracy = 0
    for each_accuracy in accuracy_list:
        if each_accuracy[0] == name:
            accuracy = round((math.fabs(float(each_accuracy[1]) - total_distance) / float(each_accuracy[1])) * 100, 2) # Calculate the accuracy of the tour
            
    
    return round(total_distance, 3), accuracy # Return the total distance of the tour rounded to 3 decimal places and the accuracy of the tour




############################################################################################################
###### These functions are used to get the tour data and the total distance of the tour for the given ######
######                       json file and algorithm.                                                 ######  
############################################################################################################



# This function returns the total distance of the tour and tour edges given the correct json file name and the miller tucker zemlin algorithm.
def get_tour_distance_and_edges_using_mtz(file_name, time_limit, min_gap, tee_value, algorithm="Miller Tucker Zemlin"):

    # Check if algorithm is Miller Tucker Zemlin and perform the Miller Tucker Zemlin to find the tour
    if algorithm == "Miller Tucker Zemlin":
            print("Solving the model for the json file: " + file_name.split("/")[-1] + " with the given time limit and minimum gap...")

            (name,n,d) = json_helper.get_instance(file_name) # Get the instance from the file including the number of nodes and the distance matrix
            m = n*(n-1)/2 # Number of edges in a complete graph.
            model = mtz.get_pyomo_model(n,m,d) # Get the Pyomo model
            mtz.set_objective_function(model) # Set the objective function
            mtz.set_constraints(model, n) # Set the constraints

            distance, tour_edges = mtz.solve(model, time_limit, min_gap, tee_value) # Solve the model
            
            return distance, tour_edges
            
    
    # If algorithm not recognised, return None
    else:
        return None

# This function returns the total distance of the tour given the correct json file name and the miller tucker zemlin algorithm.
def single_json_file_tour_edges_total_distance(file_name, time_limit=300, min_gap=0.01, tee_value=0, algorithm=None):

    # Check if algorithm is Miller Tucker Zemlin and perform the Miller Tucker Zemlin to find the tour
    if algorithm == "Miller Tucker Zemlin":
        print("Calculating the time taken to find the distance of the " + algorithm + " tour for the json file...")
        distance, tour_edges = get_tour_distance_and_edges_using_mtz(file_name, time_limit, min_gap, tee_value, algorithm)

        name = file_name.split("/")[-1].replace(".json", "")# Get the name of the file

        # Check if the file is in the accuracy list
        accuracy = 0
        for each_accuracy in accuracy_list:
            if each_accuracy[0] == name:
                accuracy = (math.fabs(float(each_accuracy[1]) - distance) / float(each_accuracy[1])) * 100 # Calculate the accuracy of the tour


        return distance, accuracy
    # If algorithm not recognised, return None
    else:
        return None





############################################################################################################
###### These functions are used to plot graphs for the benchmarking of the algorithms ######################
######    and to plot the tour on the graph for the given tsp file and algorithm.     ######################
############################################################################################################

# This function plots the benchmark graph for the given tsp directory and algorithm and calls the callback function.
def tsp_directory_plot_benchmark_graph(directory, algorithm, callback=None):
    print("Calculating the time taken to find the " + algorithm + " tour for each tsp file in the directory...")

    total_start_time = time.time()

    tsp_file_data_list = []
    times = []
    nodes = []

    
    for each_file in os.listdir(directory):
        if each_file.endswith('.tsp'):
            
            start_time = time.time()
            
            tsp_file_data = single_tsplib_file_tour_data(directory + each_file, algorithm)
            

            number_of_nodes = tsp_file_data[2]
            end_time = time.time()
            total_time_taken = round(end_time - start_time, 3)
            
            tsp_file_data_list.append(tsp_file_data)
            times.append(total_time_taken)
            nodes.append(number_of_nodes)
    

    print()
    total_time = round(time.time() - total_start_time, 3)
    print("Total Time Taken: " + str(total_time) + " seconds(s)")

    if callback:
        callback()

    return nodes, times, algorithm

def plot_benchmark_graph(nodes, times, algorithm, callback=None, marker='x', color='b', linestyle='', linewidth=0.5):
    if callback:
        callback()

    plt.plot(nodes, times, marker=marker, color=color, linestyle=linestyle, linewidth=linewidth)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Time Taken (s)')
    plt.title("Time Taken to Find " + algorithm + " Tour for Each TSP File")
    plt.show()





# This function plots the tour on the graph.
def tsp_file_plot_tour(file_name, algorithm, callback=None):
    print("Plotting the " + algorithm + " tour for the tsp file...")

    tour_graph = nx.Graph() # Create a new graph
    tsp_data = single_tsplib_file_tour_data(file_name, algorithm) # Get the tour edges for the file using the given algorithm
    if algorithm == "Nearest Neighbour":
        tour_graph.add_nodes_from(tsp_data[3]) # Add nodes to the graph
        G = tsp_data[1] # Get the graph
        nodes = tsp_data[4] # Get the nodes
        my_pos = {i: (nodes[i][0], nodes[i][1]) for i in G.nodes()} # Get the position of the nodes
    else:
        tour_graph.add_nodes_from(tsp_data[5]) # Add nodes to the graph
        my_pos = tsp_data[4] # Get the position of the nodes

    tour_graph.add_edges_from(tsp_data[0]) # Add edges to the graph

    if callback:
        callback()

    distance = 0 # Initialise the total distance of the tour to 0

    # Check if algorithm is Large Neighbourhood Search Convergence and return the total distance of the tour which is the 7th element in the tuple
    if algorithm == "Large Neighbourhood Search Convergence":
        distance = tsp_data[6]
    
    # Check if algorithm is not Nearest Neighbour and return the total distance of the tour
    elif algorithm != "Nearest Neighbour":
        tour_edge = tsp_data[0]
        for i, j in tour_edge:
            G = tsp_data[1]
            distance += tsp_data[3][(i, j)]
    
    # Check if algorithm is Nearest Neighbour and return the total distance of the tour
    elif algorithm == "Nearest Neighbour":
        tour_edge = tsp_data[0]
        for i, j in tour_edge:
            G = tsp_data[1]
            distance += G[i][j]['weight']


    plt.figure(figsize=(8, 6)) # Set the size of the plot
    nx.draw(tour_graph, pos=my_pos, with_labels=True, node_size=200, font_size=10) # Draw the graph

    # Set distance text below graph and set title
    fig = plt.gcf()
    fig.text(0.5, 0.05, "Total Distance: {:.2f}".format(distance), horizontalalignment='center', verticalalignment='center')
    fig.text(0.5, 0.95, "Algorithm: " + algorithm + "\n" + "File: " + file_name.split("/")[-1], horizontalalignment='center', verticalalignment='center')

    plt.show() # Show the plot

# This function returns the graph for the given tsp file and algorithm for the given subplot ax without plotting the graph
def tsp_file_plot_tour_for_subplots(file_name, ax, algorithm):
    print("Plotting the " + algorithm + " tour for the tsp file...")

    tour_graph = nx.Graph() # Create a new graph
    tsp_data = single_tsplib_file_tour_data(file_name, algorithm) # Get the tour edges for the file using the given algorithm
    if algorithm == "Nearest Neighbour":
        tour_graph.add_nodes_from(tsp_data[3]) # Add nodes to the graph
        G = tsp_data[1] # Get the graph
        nodes = tsp_data[4] # Get the nodes
        my_pos = {i: (nodes[i][0], nodes[i][1]) for i in G.nodes()} # Get the position of the nodes
    else:
        tour_graph.add_nodes_from(tsp_data[5]) # Add nodes to the graph
        my_pos = tsp_data[4] # Get the position of the nodes

    tour_graph.add_edges_from(tsp_data[0]) # Add edges to the graph

    # plt.figure(figsize=(8, 6)) # Set the size of the plot
    nx.draw(tour_graph, pos=my_pos, with_labels=True, node_size=200, font_size=10, ax=ax) # Draw the graph

    return tsp_data # Return the tsp data
    
    


# This function returns the graph from the tour edges.
def get_graph_from_tour_edges(tour_edges):
    G = nx.Graph()
    G.add_edges_from(tour_edges)
    return G


############################################################################################################
###### These functions are used to plot graphs for the benchmarking of the algorithms ######################
###### and to plot the tour on the graph for the given json file/directory and algorithm. ##################
############################################################################################################

# This function plots the benchmark graph for the given json directory and algorithm.
def json_directory_plot_benchmark_graph(directory, chosen_time_limit, chosen_min_gap, tee_value, algorithm):
    print("Calculating the time taken to find the " + algorithm + " tour for each json file in the directory...")

    total_start_time = time.time()

    tour_edges_list = []
    times = []
    nodes = []
    
    if algorithm == "Miller Tucker Zemlin":
        for each_file in os.listdir(directory):
            if each_file.endswith('.json'):
                start_time = time.time()
                distance, json_file_edges = get_tour_distance_and_edges_using_mtz(directory + each_file, chosen_time_limit, chosen_min_gap, tee_value, algorithm)
                end_time = time.time()
                total_time_taken = round(end_time - start_time, 3)
                tour_edges_list.append(json_file_edges)
                times.append(total_time_taken)

    print()
    total_time = round(time.time() - total_start_time, 3)
    print("Total Time Taken: " + str(total_time) + " seconds(s)")

    plt.plot(nodes, times, marker='x', color='b', linestyle='', linewidth=0.5)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Time Taken (s)')
    plt.title("Time Taken to Find " + algorithm + " Tour for Each Json File")
    plt.show()


# This function plots the tour on the graph for json files.
def json_file_plot_tour(file_name, chosen_time_limit=300, chosen_min_gap=0.01, tee_value=0, algorithm="Miller Tucker Zemlin", callback=None):
    print("Plotting the " + algorithm + " tour for the json file...")

    # Change file type to .tsp and assign to tsp_file_name
    tsp_file_name = file_name.replace("Miller_Tucker_Zemlin/json_files/", "tsp/tsp_library/").replace(".json", ".tsp")
    my_pos = get_node_positions(tsp_file_name) # Get the position of the nodes

    distance, tour_edges = get_tour_distance_and_edges_using_mtz(file_name, chosen_time_limit, chosen_min_gap, tee_value, algorithm) # Get the tour edges for the file using the given algorithm
    if algorithm == "Miller Tucker Zemlin":
        G = get_graph_from_tour_edges(tour_edges) # Get the graph from the tour edges

    
        # Create a new graph for the tour
        tour_graph = nx.Graph()
        
        # Add nodes to the tour graph
        for node in G.nodes():
            tour_graph.add_node(node)
        
        # Add edges corresponding to the tour to the tour graph
        tour_graph.add_edges_from(tour_edges)

        if callback:
            callback()
        
        # Draw the original graph with nodes and edges
        nx.draw(G, my_pos, with_labels=True)
        
        # Draw the tour edges in red
        nx.draw_networkx_edges(tour_graph, my_pos, edgelist=tour_edges, edge_color='r', width=2)
        
        # Set distance text below graph and set title
        fig = plt.gcf()
        fig.text(0.5, 0.05, "Total Distance: {:.2f}".format(distance), horizontalalignment='center', verticalalignment='center')
        fig.text(0.5, 0.95, "Algorithm: " + algorithm + "\n" + "File: " + file_name.split("/")[-1], horizontalalignment='center', verticalalignment='center')

        # Show the plot
        plt.show()

# This function returns the graph for json files for the given subplot ax without plotting the graph
def json_file_plot_tour_for_subplots(file_name, ax, chosen_time_limit=300, chosen_min_gap=0.01, tee_value=1, algorithm="Miller Tucker Zemlin"):
    print("Plotting the " + algorithm + " tour for the json file...")

    # Change file type to .tsp and assign to tsp_file_name
    tsp_file_name = file_name.replace("Miller_Tucker_Zemlin/json_files/", "tsp/tsp_library/").replace(".json", ".tsp")
    my_pos = get_node_positions(tsp_file_name) # Get the position of the nodes

    distance, tour_edges = get_tour_distance_and_edges_using_mtz(file_name, chosen_time_limit, chosen_min_gap, tee_value, algorithm) # Get the tour edges for the file using the given algorithm
    if algorithm == "Miller Tucker Zemlin":
        G = get_graph_from_tour_edges(tour_edges) # Get the graph from the tour edges
    
        # Create a new graph for the tour
        tour_graph = nx.Graph()
        
        # Add nodes to the tour graph
        for node in G.nodes():
            tour_graph.add_node(node)
        
        # Add edges corresponding to the tour to the tour graph
        tour_graph.add_edges_from(tour_edges)
        
        nx.draw(tour_graph, pos=my_pos, with_labels=True, node_size=200, font_size=10, ax=ax) # Draw the graph

        return distance

        


############################################################################################################
###########     These functions are used to plot two graphs compared to each other          ################
############################################################################################################

# This function plots two graphs compared to each other for the given file and algorithm.
def plot_two_graphs_compared_to_each_other(file_name, first_algorithm, file_name2, second_algorithm, callback=None):
    print("Plotting the " + first_algorithm + " and " + second_algorithm + " tours for the json file...")

    # Set the size of the plot
    plt.figure(figsize=(15, 10))  # Adjust the width and height as needed

    # Create separate subplots for each graph
    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)

    if first_algorithm == "Miller Tucker Zemlin":
        first_distance = json_file_plot_tour_for_subplots(file_name, ax=ax1)
    else:
        tsp_data_1 = tsp_file_plot_tour_for_subplots(file_name, ax=ax1, algorithm=first_algorithm)
        first_distance = 0 # Initialise the total distance of the tour to 0

        # Check if algorithm is Large Neighbourhood Search Convergence and return the total distance of the tour which is the 7th element in the tuple
        if first_algorithm == "Large Neighbourhood Search Convergence":
            first_distance = tsp_data_1[6]

        # Check if algorithm is not Nearest Neighbour and return the total distance of the tour
        elif first_algorithm != "Nearest Neighbour":
            tour_edge = tsp_data_1[0]
            for i, j in tour_edge:
                G = tsp_data_1[1]
                first_distance += tsp_data_1[3][(i, j)] 

        # Check if algorithm is Nearest Neighbour and return the total distance of the tour
        elif first_algorithm == "Nearest Neighbour":
            tour_edge = tsp_data_1[0]
            for i, j in tour_edge:
                G = tsp_data_1[1]
                first_distance += G[i][j]['weight']


    if second_algorithm == "Miller Tucker Zemlin":
        second_distance = json_file_plot_tour_for_subplots(file_name2, ax=ax2)
    else:
        tsp_data_2 = tsp_file_plot_tour_for_subplots(file_name2, ax=ax2, algorithm=second_algorithm)
        second_distance = 0

        # Check if algorithm is Large Neighbourhood Search Convergence and return the total distance of the tour which is the 7th element in the tuple
        if second_algorithm == "Large Neighbourhood Search Convergence":
            second_distance = tsp_data_2[6]
        
        # Check if algorithm is not Nearest Neighbour and return the total distance of the tour
        elif second_algorithm != "Nearest Neighbour":
            tour_edge = tsp_data_2[0]
            for i, j in tour_edge:
                G = tsp_data_2[1]
                second_distance += tsp_data_2[3][(i, j)]
        
        # Check if algorithm is Nearest Neighbour and return the total distance of the tour
        elif second_algorithm == "Nearest Neighbour":
            tour_edge = tsp_data_2[0]
            for i, j in tour_edge:
                G = tsp_data_2[1]
                second_distance += G[i][j]['weight']
        

    

    if callback:
        callback()
    
    # Set title for the first graph
    ax1.set_title(first_algorithm + " Tour")

    # Set title for the second graph
    ax2.set_title(second_algorithm + " Tour")

    

    # Add total distance text under each graph
    ax1.text(0.5, -0.1, "Total Distance: {:.2f}".format(first_distance), horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes)
    ax2.text(0.5, -0.1, "Total Distance: {:.2f}".format(second_distance), horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes)

    plt.tight_layout()
    plt.show()



############################################################################################################
###### These functions are used to get the tour edges and the total distance of the all the tours for ######
######                         for the given tsp directory and algorithm.                           ########
############################################################################################################

# This function returns the tour edges for each file in the tsp directory using the given algorithm in a list.
def tsp_directory_tour_edges(tsp_directory, algorithm):
    tour_edges_list = []
    for each_file in os.listdir(tsp_directory):
        if each_file.endswith('.tsp'):
            tsp_file_edges = single_tsplib_file_tour_data(tsp_directory + each_file, algorithm)
            tour_edges_list.append(tsp_file_edges)
    return tour_edges_list

# This function returns the total distance of the tour for each file in the tsp directory using the given algorithm in a list.
def tsp_directory_tour_edges_total_distance(tsp_directory, algorithm):
    tour_edges_list = tsp_directory_tour_edges(tsp_directory, algorithm) # Get the tour edges for each file in the tsp directory using the given algorithm in a list
    for tour_edges in tour_edges_list:
        total_distance = 0
        # Total distance of the tour
        tour_edge = tour_edges[0]
        for i, j in tour_edge:
            G = tour_edges[1]
            total_distance += G[i][j]['weight']
        print(round(total_distance, 3))


############################################################################################################
######          This function is used to get the tour edges for the given tour and graph            ########
############################################################################################################
        
# This function returns the edges of the tour.
def get_tour_edges(tour, G):
    return [(tour[i-1], tour[i]) for i in range(G.number_of_nodes())]


def get_similar_files(first_directory, second_directory):
    first_files = []
    second_files = []
    similar_files = []
    for each_file in (first_directory):
        if each_file.endswith('.tsp') or each_file.endswith('.json'):
            first_files.append(each_file.split('.')[0])
    for each_file in (second_directory):
        if each_file.endswith('.tsp') or each_file.endswith('.json'):
            second_files.append(each_file.split('.')[0])
    for file in first_files:
        if file in second_files:
            similar_files.append(file)
    return similar_files
