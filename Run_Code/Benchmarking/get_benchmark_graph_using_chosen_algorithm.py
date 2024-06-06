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
import Code.Helper_Methods.json_library_helper as jsonlib
import Code.Helper_Methods.input as input

def run_benchmark():
    algorithm = input.chosen_algorithm()

    if algorithm == "Miller Tucker Zemlin":
        directory = jsonlib.get_json_files_directory()
        chosen_time_limit, chosen_min_gap, tee_value = input.get_mtz_values()
        tsp.json_directory_plot_benchmark_graph(directory, chosen_time_limit, chosen_min_gap, tee_value, algorithm)

    else:
        directory = tsplib.get_tsp_lib_directory()
        nodes, times, algo = tsp.tsp_directory_plot_benchmark_graph(directory, algorithm)
        tsp.plot_benchmark_graph(nodes, times, algo)
    

if __name__ == "__main__":
    run_benchmark()
