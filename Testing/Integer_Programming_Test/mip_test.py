import sys
sys.path.append("../")
from Code.Miller_Tucker_Zemlin.mip_solver import solve, get_pyomo_model, set_constraints, set_objective_function

import numpy as np
import networkx as nx
import gurobipy as gp
from pyomo.environ import *
from pyomo.opt import SolverFactory


def test_solve():
    # Define the model
    n = 3  # Number of nodes
    d = np.array([[0, 1, 2], [1, 0, 3], [2, 3, 0]])  # Distance matrix
    m = n*(n-1)/2  # Number of edges
    model = get_pyomo_model(n, m, d)
    
    # Set the objective function
    set_objective_function(model)

    # Set the constraints
    set_constraints(model, n)
    
    # Set parameters for testing
    time_limit = 3600  # 1 hour time limit
    mip_gap = 0.05  # MIP gap tolerance
    tee_value = False  # Set to True to print solver log
    
    # Call the solve function
    objective_value, tour_edges = solve(model, time_limit, mip_gap, tee_value)
    
    # Assertion: Check if the solve function returns valid results
    assert objective_value is not None, "Objective value should not be None"
    assert tour_edges is not None, "Tour edges should not be None"
    assert len(tour_edges) == len(model.V) == 3, "Number of tour edges should match number of nodes"

# Run the test
test_solve()