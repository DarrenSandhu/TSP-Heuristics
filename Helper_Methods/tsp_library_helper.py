import os
import numpy as np
import re


# Return current working directory
def get_current_working_directory():
    return os.getcwd()

# Return tsp directory
def get_tsp_lib_directory():
    return get_current_working_directory() + "/tsp/tsp_library/"

# Return list of files from tsp directory
def get_tsp_lib_files_from_directory():
    tsp_directory = get_tsp_lib_directory()
    tsp_files = []
    for root, dirs, files in os.walk(tsp_directory):
        for file in files:
            if file.endswith(".tsp"):
                tsp_files.append(file)
    return tsp_files    

