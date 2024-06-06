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
import Code.Helper_Methods.input as input

algorithm = input.chosen_algorithm()

if algorithm == "Miller Tucker Zemlin":
    file, chosen_time_limit, chosen_min_gap, tee_value = input.chosen_tsp_file(algorithm)
    tsp.json_file_plot_tour(file, chosen_time_limit, chosen_min_gap, tee_value, algorithm)
else:   
    file = input.chosen_tsp_file(algorithm)
    tsp.tsp_file_plot_tour(file, algorithm)

