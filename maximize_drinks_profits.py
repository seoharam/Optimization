import pulp as pl 
from tqdm import tqdm
import math

# region : Problem set
####################################
# 2가지 종류의 주스를 생산할 때 순수익을 최대화하는 문제
####################################
# endregion

# region : sets (about decision variable index)
####################################
# index 0 is Apple-Mango Juice, index 1 is Orange-Berry Juice 
I = [0, 1]
####################################
# endregion

# region : parameters (about data that was inserted)
####################################
# Net profits of AM and OB
P = [7, 9]
# Stocks of Apples, Mangos, Oranges, Berries
S = [(100, 50), (90, 80)]
# Maximum capacity of production
M_C = 60
# Material number of each juice
M = [(2, 1), (3, 2)]
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
    objective_function += X[i] * P[i]
model += objective_function
####################################
# endregion

# region : constraints (about condition of decision variable)
####################################
# 1). Apple-Mango juice and Orange-Berry juice must be made until number of M_C 
temp = []
for i in I:
    temp.append((X[i], 1))
const1_left = pl.LpAffineExpression(temp)
model += const1_left <= M_C

# 2). material number of apples is smaller than stocks of apples
const2_left = M[0][0]*X[0]
model += const2_left <= S[0][0]

# 3). material number of mangos is smaller than stocks of mangos
const3_left = M[0][1]*X[0]
model += const3_left <= S[0][1]

# 4). material number of oranges is smaller than stocks of oranges
const4_left = M[1][0]*X[1]
model += const4_left <= S[1][0]

# 5). material number of berries is smaller than stocks of berries
const5_left = M[1][1]*X[1]
model += const5_left <= S[1][1]
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