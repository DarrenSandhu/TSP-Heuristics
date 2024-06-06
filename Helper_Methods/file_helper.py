import os
import numpy as np
import re

# Return list of lines.
def read_file(file_name):
	with open(file_name) as f:
		lines = f.read().splitlines()
	return lines

def get_instance(file_lines):
    
    # Check if string s contains any alphabetic character.
    def contains_alpha(s):
        return bool(re.search('[a-zA-Z]', s))

    nodes = [] # To be populated with the node coordinates.
    name = '' # The name of the instance.
    n = 0 # The number of nodes.
    correct_format = False

    for l in file_lines:
        
        # The line with string 'NAME' contains the instance name.
        if 'NAME' in l:
            name = l.split(":")[1]

        # The line with the string 'DIMENSION' contains the number of nodes.
        if 'DIMENSION' in l:
            n = int(l.split(":")[1])

        # Every line not containing an alphabetic character, contains the coordinates of a node.
        if not contains_alpha(l):
            values = l.split()
            if len(values) >= 3:  # Check if there are at least three values in the line
                x = float(values[1])
                y = float(values[2])
                nodes.append([x, y])
    
    if len(nodes) != n:
        print("The number of nodes does not match the number of coordinates for file name: ${name}.")
        return (name, n, nodes, correct_format)
    
    
    nodes = np.array(nodes)
    correct_format = True

    return (name, n, nodes, correct_format)

def get_all_instances_from_directory():
    directory = "tsp/tsp_library/"
    instances = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".tsp"):
                file_lines = read_file(directory + file)
                instance = get_instance(file_lines)
                if instance[3]:
                    instances.append(instance)
    return instances
