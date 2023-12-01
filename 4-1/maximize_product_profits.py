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
# product type indexed by i
I = [0, 1]
####################################
# endregion

# region : parameters (about data that was inserted)
####################################
# manufactoring cost of product type i
C = [10, 15]
# manufactoring hours of product type i
T = [1,2]
# Revenue of product type i
P = [20, 30]
# Maximum cost of material
M_C = 40
# Maximum hours of work
M_H = 8
####################################
# endregion

# region : decision variables (about answer we have to know for solving linear problem)
####################################
# 0 = chair, 1 = table
X = []
for i in I:
    X.append(pl.LpVariable('x_' + str(i), lowBound=0, cat = pl.LpContinuous))
####################################
# endregion

# region : model (about Purpose in problem)
####################################
model = pl.LpProblem('Maximize_net_profits', pl.LpMaximize)
####################################
# endregion

# region : objective function (about function to solve this problem)
####################################
objective = []
for i in I:
    objective.append((X[i], P[i] - C[i]))
objective_function = pl.LpAffineExpression(objective)
model += objective_function
####################################
# endregion

# region : constraints (about condition of decision variable)
####################################
# 1). constraint : all of cost for manufactoring product tpye i have upper cost limit
temp = []
for i in I:
    temp.append((X[i], C[i]))
const1 = pl.LpAffineExpression(temp)
model += const1 <= M_C

# 2). constraint: all of hours for manufactoring product type i have upper hours limit
temp = []
for i in I:
    temp.append((X[i], T[i]))
const2 = pl.LpAffineExpression(temp)
model += const2 <= M_H
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