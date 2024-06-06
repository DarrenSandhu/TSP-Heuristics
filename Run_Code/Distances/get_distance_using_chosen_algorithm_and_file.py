import time
import networkx as nx
import random
import matplotlib.pyplot as plt
import math 
import numpy as np
import re
import os
import sys
sys.path.append("../")

import Code.Helper_Methods.input as input
import Code.Helper_Methods.tsp_helper as tsp

algorithm = input.chosen_algorithm()

start_time = 0

if algorithm == "Miller Tucker Zemlin":
    file, chosen_time_limit, chosen_min_gap, tee_value = input.chosen_tsp_file(algorithm)
    start_time = time.time()
    distance, tour_edges = tsp.get_tour_distance_and_edges_using_mtz(file, chosen_time_limit, chosen_min_gap, tee_value, algorithm)
else:   
    file = input.chosen_tsp_file(algorithm)
    start_time = time.time()
    distance = tsp.single_tsp_file_tour_edges_total_distance(file, algorithm)

print("Total Time Taken: "+ str(round(time.time() - start_time, 3)) + " seconds(s)")
print("Distance: "+ str(distance[0]))
print("Accuracy: "+ str(distance[1]) + "%")