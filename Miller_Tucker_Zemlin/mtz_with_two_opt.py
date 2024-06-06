import numpy as np
import networkx as nx
import gurobipy as gp
from pyomo.environ import *
from pyomo.opt import SolverFactory

############################################################
#### This whole code was provided by my supervisor ######### 
############################################################
def get_pyomo_model(n,m,d):
    
    model = AbstractModel()
    model.n = Param(within = NonNegativeIntegers, initialize = n) # Number of nodes.
    model.V = RangeSet(0,n-1) # Set of vertices.
    model.d = Param(model.V*model.V, within = NonNegativeIntegers, initialize = lambda model, i, j: d[i,j]) # Edge distances.
    model.x = Var(model.V*model.V, within = Binary)
    model.u = Var(model.V, within = NonNegativeReals) 
    return model

def set_objective_function(model):

    def tour_length_objective_rule(model):
        return sum(sum(model.x[i,j]*model.d[i,j] for i in model.V) for j in model.V) 
    model.obj_value = Objective(rule = tour_length_objective_rule, sense = minimize)

def set_constraints(model, n):

    # The tour has exactly one exiting edge from each node i.
    def exiting_rule(model, i):
        return sum(model.x[i,j] for j in model.V if i!=j) == 1 
    model.exiting_constraint = Constraint(model.V, rule = exiting_rule)   

    # The tour has exactly one entering edge at each node j.
    def entering_rule(model, j):
        return sum(model.x[i,j] for i in model.V if i!=j) == 1 
    model.entering_constraint = Constraint(model.V, rule = entering_rule)  

    def first_vertex_position_rule(model):
        return model.u[0] == 1
    model.first_vertex_position_constraint = Constraint(rule = first_vertex_position_rule)

    def vertex_position_rule(model,i,j):
        if i != 1:
            return model.u[i] - model.u[j] + model.x[i,j] * n <= n-1
        else:
            return Constraint.Skip
    model.vertex_position_rule = Constraint(model.V, model.V, rule = vertex_position_rule)

    def next_vertex_positions_lower_bound_rule(model, i):
        if i != 0:
            return model.u[i] >= 2
        else:
            return Constraint.Skip
    model.next_vertex_positions_lower_bound_constraint = Constraint(model.V, rule = next_vertex_positions_lower_bound_rule)

    def next_vertex_positions_upper_bound_rule(model, i):
        if i != 0:
            return model.u[i] <= model.n
        else:
            return Constraint.Skip
    model.next_vertex_positions_upper_bound_constraint = Constraint(model.V, rule = next_vertex_positions_upper_bound_rule)

# This function finds a tour using the 2-opt local search heuristic.
def two_opt_local_search(G, distances, n):
	improved = True
	tour = list(G.nodes())

	while improved:
		improved = False
		for i in range(n):
			for j in range(i+1, n):
				currentEdge1 = (tour[i], tour[(i+1)])
				currentEdge2 = (tour[j], tour[(j+1)%n])
                    
				newEdge1 = (tour[i], tour[j])
				newEdge2 = (tour[(i+1)], tour[(j+1)%n])
                    
				currentEdgesDistance = distances[currentEdge1] + distances[currentEdge2]
				newEdgesDistance = distances[newEdge1] + distances[newEdge2]

				if newEdgesDistance < currentEdgesDistance:
					tour[i+1:j+1] = tour[i+1:j+1][::-1]
					improved = True
	return tour


def solve(model, time_limit, mip_gap, tee_value):

    opt = SolverFactory('gurobi')
    
    opt.options['TimeLimit'] = time_limit
    opt.options['MIPGap'] = mip_gap

    pyomo_instance = model.create_instance()
    pyomo_result = opt.solve(pyomo_instance, tee = tee_value)  # Set tee=True to print solver log

    tour_edges = [] # List of edges in the tour

    # Check if the optimization was successful
    if pyomo_result.solver.status == SolverStatus.ok and pyomo_result.solver.termination_condition == TerminationCondition.optimal:
        # Print best objective value and gap
        print("Solver found an optimal solution.")
        objective_value = pyomo_result.Problem.upper_bound
        print()
        print("Best Objective Value:", objective_value)
        print()

        # Extract the tour edges from the Pyomo model instance
        for i in pyomo_instance.V:
            for j in pyomo_instance.V:
                if pyomo_instance.x[i, j].value == 1:
                    tour_edges.append((i, j))
        print("Tour Edges:", tour_edges)
        return objective_value, tour_edges
    else:
        print("Solver did not find an optimal solution.")
        print()
        objective_value = pyomo_result.Problem.upper_bound
        print("Objective Value:", objective_value)
        print()

        for i in pyomo_instance.V:
            for j in pyomo_instance.V:
                if pyomo_instance.x[i, j].value == 1:
                    tour_edges.append((i, j))

        print("Tour Edges:", tour_edges)
        return objective_value, tour_edges
