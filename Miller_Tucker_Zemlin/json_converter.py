import re
import numpy as np
from scipy.spatial import distance_matrix
from scipy.special import round
import json
############################################################
#### This whole code was provided by my supervisor ######### 
############################################################
# Return list of lines.
def read_file(file_name):
	with open(file_name) as f:
		lines = f.read().splitlines()
	return lines

# Return the tsp file in jason format.
def get_tsp_instance(file_lines):

	# Check if string s contains any alphabetic character.
	def contains_alpha(s):
		return bool(re.search('[a-zA-Z]', s))

	nodes = [] # To be populated with the node coordinates.
	name = '' # The name of the instance.
	n = 0 # The number of nodes.

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

	nodes = np.array(nodes)

	return (name,n,nodes)

def serialize_to_json(name,n,edges):

	file_name = 'Code/Miller_Tucker_Zemlin/json_files/' + name + '.json'	
	dictionary = {'name':name, 'n':n, 'd':edges.tolist()}
	json_object = json.dumps(dictionary,indent=4)
	with open(file_name, 'w') as f:
		f.write(json_object)



	
		
	



