from pyomo.environ import *
from pyomo.opt import SolverFactory
############################################################
#### This whole code was provided by my supervisor ######### 
############################################################

m = 2 
n = 4 # there are 4 jobs which ar numbered 0,1,2,3
d = [1,2,3,4]
precedence_constraints = [(0,3),(2,3)] # this constraints mean that job 0 should be executed before job 3

model = AbstractModel()

# Parameters

# Number of jobs
model.n = Param(within = NonNegativeIntegers, initialize = n) 

# Number of machines
model.m = Param(within = NonNegativeIntegers, initialize = m) 

# Set of jobs
model.J = RangeSet(0, n-1)
	
# Set of machines
model.M = RangeSet(0, m-1)

# Job durations
model.d = Param(model.J, within = NonNegativeIntegers, initialize = lambda model, j: d[j])

# Variable which specifies whether job j is assigned to machine i
model.x = Var(model.M*model.J, within = Binary)

model.T = Var(within = NonNegativeIntegers)

# Objective: minimize makespan
def makespan_objective_rule(model):
	return model.T
model.obj_value = Objective(rule = makespan_objective_rule, sense = minimize)

# Constraint: vehicles enumeration
def makespan_rule(model, i):
	return model.T >= sum(model.x[i,j]*model.d[j] for j in model.J) 
model.makespan_constraint = Constraint(model.M, rule = makespan_rule)   

# Constraint: vehicles enumeration
def assignment_rule(model, j):
	return sum(model.x[i,j] for i in model.M) == 1 
model.assignment_constraint = Constraint(model.J, rule = assignment_rule)   


opt = SolverFactory('gurobi')
# opt.options['threads'] = 1
# opt.options['logfile'] = None
#opt.options['mipgap'] = solver_config.relative_gap_tolerance
# opt.options['timelimit'] = 3600

pyomo_instance = model.create_instance()
pyomo_result = opt.solve(pyomo_instance)

T = int(pyomo_instance.T.value)
x = [[pyomo_instance.x[i,j].value for i in range(m)] for j in range(n)]

print('Makespan: ' + str(T))




