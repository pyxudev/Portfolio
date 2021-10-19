import pyomo.environ as pyo
import math

model = pyo.ConcreteModel(name="autoestimation", doc="2 float")
model.x = pyo.Var([1,2], domain=pyo.NonNegativeReals, bounds=(0.1, 1.0))

cols = 10 
rows = 1000000
date = 7

model.OBJ = pyo.Objective(expr = model.x[1]*math.log10(cols) + model.x[2]*(math.log10(rows)/math.sqrt(date/30)), sense = pyo.maximize)
model.Constraint = pyo.Constraint(expr = model.x[1] + model.x[2] <= 1)

opt = pyo.SolverFactory('ipopt')
res = opt.solve(model)

print(f"評価関数：{model.OBJ()}")
print(f"x1: {model.x[1]()}")
print(f"x2: {model.x[2]()}")