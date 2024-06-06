import numpy as np
import os
import sys
sys.path.append("../")

import Code.Helper_Methods.tsp_library_helper as tsp_lib
import Code.Helper_Methods.json_library_helper as json_lib
# Return chosen tsp file from input from user
def choose_json_file(json_files):
    while True:
        chosen_tsp_file = input("Enter the name of the tsp file you want to use (e.g. ulysses16): ")

        # Check if chosen json file is in the list of json files
        if chosen_tsp_file + ".json" in json_files:
            return chosen_tsp_file + ".json"
        
        # If not, print error message
        else:
            print("Invalid file name. Please try again.")
            print()

# Return chosen time limit from input from user
def choose_time_limit():
    while True:
        chosen_time_limit = input("Enter the time limit for the solver (default is 300 seconds, press enter to use recommended default): ")

        # Check if time limit is a number
        if chosen_time_limit.isdigit():
            return int(chosen_time_limit)
        
        # Check if time limit is empty and then set to default value
        elif chosen_time_limit == "":
            return 300
        
        # If not, print error message
        else:
            print("Invalid time limit. Please enter a number.")
            print()

# Return chosen minimum gap from input from user
def choose_min_gap():
    while True:
        chosen_min_gap = input("Enter the minimum gap for the solver (default is 0.01 which is 1%, press enter to use recommended default): ")
        try:
            # Check if minimum gap is empty and then set to default value
            if chosen_min_gap == "":
                return 0.01
            
            min_gap = float(chosen_min_gap) # Convert to float

            # Check if minimum gap is between 0 and 1
            if 0 <= min_gap <= 1:
                return min_gap
            
            # If not, print error message
            else:
                print("Invalid minimum gap. Please enter a number between 0 and 1.")
        except ValueError:
            print("Invalid minimum gap. Please enter a number between 0 and 1.")
        print()

# Return chosen tee value from input from user
def choose_tee_value():
    while True:
        tee_value = input("Would you like to print the solver log? (1 for yes, 0 for no, press enter to use recommended default which is false): ")
        if tee_value == "1":
            return True
        elif tee_value == "0" or tee_value == "":
            return False
        else:
            print("Invalid tee value. Please enter 1 or 0.")
        print()

# Return values needed for miller tucker zemlin
def get_mtz_values():
    chosen_time_limit = choose_time_limit()
    print()
    chosen_min_gap = choose_min_gap()
    print()
    tee_value = choose_tee_value()
    print()
    return chosen_time_limit, chosen_min_gap, tee_value

# Return chosen file data
def get_chosen_json_file_data():
    json_files = json_lib.get_json_files_from_directory()
    json_directory = json_lib.get_json_files_directory_no_cwd()
    
    json_lib.print_json_files(json_files)

    print()
    chosen_json_file = choose_json_file(json_files)
    print()
    chosen_time_limit, chosen_min_gap, tee_value = get_mtz_values()
    
    
    print()
    print("Chosen tsp file: " + chosen_json_file)
    print("Chosen time limit: " + str(chosen_time_limit) + " seconds")
    print("Chosen minimum gap: " + str(float(chosen_min_gap) * 100) + "%")
    print()

    return json_directory + chosen_json_file, chosen_time_limit, chosen_min_gap, tee_value


# Return chosen algorithm from input from user
def chosen_algorithm():

    print("Algorithms: \n 1. Nearest Neighbour \n 2. Nearest Neighbour Optimisation \n 3. Two Opt \n 4. Two Opt with Nearest Neighbour \n 5. Two Opt with Greedy Heuristic \n 6. Two Opt with Insertion Heuristic \n 7. Large Neighbourhood Search \n 8. Large Neighbourhood Search With Convergence \n 9. Miller Tucker Zemlin \n")
    while True:
        chosen_algorithm = input("Enter the number of the algorithm you want to use (e.g. 1 for Nearest Neighbour, 2 for Nearest Neighbour Optimisation etc): ")
        try:
            algorithm = float(chosen_algorithm) # Convert to float

            # Check algorithm is between 1 and 5
            if 1 <= algorithm <= 9:
                if algorithm == 1:
                    chosen_algorithm = "Nearest Neighbour"
                elif algorithm == 2:
                    chosen_algorithm = "Nearest Neighbour Optimisation"
                elif algorithm == 3:
                    chosen_algorithm = "Two Opt"
                elif algorithm == 4:
                    chosen_algorithm = "Two Opt with Nearest Neighbour"
                elif algorithm == 5:
                    chosen_algorithm = "Two Opt with Greedy Heuristic"
                elif algorithm == 6:
                    chosen_algorithm = "Two Opt with Insertion Heuristic"
                elif algorithm == 7:
                    chosen_algorithm = "Large Neighbourhood Search"
                elif algorithm == 8:
                    chosen_algorithm = "Large Neighbourhood Search Convergence"
                elif algorithm == 9:
                    chosen_algorithm = "Miller Tucker Zemlin"
                    mtz = True
                print()
                break
            
            # If not, print error message
            else:
                print("Invalid algorithm number. Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid algorithm number. Please enter a number between 1 and 7.")
        print()
    
    return chosen_algorithm

# Return chosen tsp file from input from user 
def chosen_tsp_file(chosen_algorithm):
    
    if chosen_algorithm == "Miller Tucker Zemlin":
        chosen_tsp_file, chosen_time_limit, chosen_min_gap, tee_value = get_chosen_json_file_data()
        print()
        return (chosen_tsp_file, chosen_time_limit, chosen_min_gap, tee_value)
    
    else:
        tsp_files = tsp_lib.get_tsp_lib_files_from_directory()
        tsp_directory = "tsp/tsp_library/"
        tsp_file_type = ".tsp"
        tsp_files.sort()
        for file in tsp_files:
            print(file.split(".")[0])
        
        print()
        while True:
            chosen_tsp_file = input("Enter the name of the tsp file you want to use: ")
            if chosen_tsp_file + tsp_file_type in tsp_files:
                print()
                break
            else:
                print("File not found, please try again")
            print()

        print()

        return (tsp_directory + chosen_tsp_file + tsp_file_type)