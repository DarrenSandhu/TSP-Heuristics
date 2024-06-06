import json
import numpy as np
import networkx as nx
import gurobipy as gp
import time
import networkx as nx
import matplotlib.pyplot as plt
import math 
import os
import sys
sys.path.append("../")

from pyomo.environ import *
from pyomo.opt import SolverFactory

import Code.Miller_Tucker_Zemlin.mip_solver as mtz

# Return current working directory
def get_cwd():
    return os.getcwd()

# Return full json directory
def get_json_files_directory():
    return get_cwd() + "/Miller_Tucker_Zemlin/json_files/"

# Return json directory without the current working directory
def get_json_files_directory_no_cwd():
    return "Miller_Tucker_Zemlin/json_files/"

# This function reads the instance from a json file.
def get_instance(file_name):
    with open(file_name) as f:
        data = json.load(f)
    name = data['name']
    n = data['n']
    d = np.array(data['d'])
    return name, n, d

# Return list of files from json directory
def get_json_files_from_directory():
    json_directory = get_json_files_directory()
    tsp_files = []
    for root, dirs, files in os.walk(json_directory):
        for file in files:
            if file.endswith(".json"):
                tsp_files.append(file)
    return tsp_files    

# Print list of json files
def print_json_files(json_files):
    for file in json_files:
        print(file.split(".")[0])





