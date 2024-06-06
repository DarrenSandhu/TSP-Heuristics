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

import Code.Helper_Methods.tsp_helper as tsp 
import Code.Helper_Methods.tsp_library_helper as tsplib

tsp_file = tsplib.chosen_tsp_file()

start_time = time.time()

tour_edges, G, n, distances, my_pos, tour = tsp.single_tsplib_file_tour_data(tsp_file, "Large Neighbourhood Search")

print("Total Time Taken: "+ str(round(time.time() - start_time, 3)) + " seconds(s)")


