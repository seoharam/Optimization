import pulp as pl 
from tqdm import tqdm
import math

# region : Problem set
####################################
# 의자와 책상을 생산할 때 최대의 순수익(net profit)을 내는 문제
####################################
# endregion

# region : sets (about decision variable index)
####################################
# index 0 is chair, index 1 is table 
I = [0, 1]
####################################
# endregion

# region : parameters (about data that was inserted)
####################################
# manufactoring cost of chair and table
C_M = [10, 15]
# manufactoring time of chair and table
T_M = [1, 2]
# profit of chair and table
P = [20, 30]
# maximum hours of work
M_H = 8
# maximum cost of material
M_C = 40
####################################
# endregion

# region : decision variables (about answer we have to know for solving linear problem)
####################################
# index 0 = number of production chairs / index 1 = number of production tables
X = []
for i in I:
    X.append(pl.LpVariable('x_' + str(i), lowBound = 0, cat = pl.LpContinuous)) 
####################################
# endregion

# region : model (about Purpose in problem)
####################################
model = pl.LpProblem('Maximize_net_profits', pl.LpMaximize)
####################################
# endregion

# region : objective function (about function to solve this problem)
####################################
objective_function = 0
for i in I:
    objective_function += X[i] * (P[i] - C_M[i])
model += objective_function
####################################
# endregion

# region : constraints (about condition of decision variable)
####################################
# 1). manufactoring cost of chair and manufactoring cost of table summation is smaller than M_C
temp = []
for i in I:
    temp.append((X[i], C_M[i]))
const1_left = pl.LpAffineExpression(temp)
model += const1_left <= M_C

# 2). manufactoring time of chair and manufactoring time of table summation is smaller than M_H
temp = []
for i in I:
    temp.append((X[i], T_M[i]))
const2_left = pl.LpAffineExpression(temp)
model += const2_left <= M_H
####################################
# endregion

# region : solve the problem
####################################
solver = pl.CPLEX_CMD()
result = model.solve(solver)

print('------------------------------------------------')
print('Result: ', result) # 1 is ok in Cplex, Others there is no solution..
print('Objective function: ', objective_function)
print("model value: ",pl.value(model.objective))
print('------------------------------------------------')
        
for i in I:
    print("X_" + str(i) + ' = ' + str(pl.value(X[i])))
    
k=1
####################################
# endregion