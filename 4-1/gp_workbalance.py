import pulp as pl 
from tqdm import tqdm
import math

# region : Problem set
####################################
# Tasks와 Resources가 있을 때 Workload를 균등히 분배하는 문제
####################################
# endregion

# region : sets (about decision variable index)
####################################
# Resources indexed by i
R = [0,1,2]
# Tasks indexed by j
T = [0,1,2,3,4]
####################################
# endregion

# region : parameters (about data that was inserted)
####################################
# Workload of Task i
W = [8,5,7,8,4]
# 1 if resource i can perform task j, 0 otherwise
A = [[1,1,1,1,0],
     [1,1,0,1,1],
     [0,1,1,1,1]]
# Maximum number of tasks that resource i can perform
M = [2,2,2]
# Goal value (same amount of workload)
G = sum(W)/len(W)
####################################
# endregion

# region : decision variables (about answer we have to know for solving linear problem)
####################################
X = []
for i in R:
    temp = []
    for j in T:
        temp.append(pl.LpVariable('X_'+str(i)+'_' + str(j), cat = pl.LpBinary))
    X.append(temp)

D_negative = []
D_positive = []

for i in R:
    D_negative.append(pl.LpVariable('D_negative_'+str(i), lowBound=0, upBound=None, cat = pl.LpContinuous))
    D_positive.append(pl.LpVariable('D_positive_'+str(i), lowBound=0, upBound=None, cat = pl.LpContinuous))
####################################
# endregion

# region : model (about Purpose in problem)
####################################
model = pl.LpProblem('Workbalance', pl.LpMinimize)
####################################
# endregion

# region : objective function (about function to solve this problem)
####################################
temp = []
for i in R:
    temp.append((D_negative[i], 1))
    temp.append((D_positive[i], 1))
objective_function = pl.LpAffineExpression(temp)
model += objective_function
####################################
# endregion

# region : constraints (about condition of decision variable)
####################################
# 1). constraint : Make a relationship between x, d, G
for i in R:
    temp = []
    for j in T:
        temp.append((X[i][j], W[j]))
    temp.append((D_negative[i], 1))
    temp.append((D_positive[i], -1))
    const1 = pl.LpAffineExpression(temp) 
    model += const1 == G

# 2). constraint : All of tasks is should be performed by a resource only one
for j in T:
    temp = []
    for i in R:
        temp.append((X[i][j],1))
    const2 = pl.LpAffineExpression(temp)
    model += const2 == 1

# 3). Each task has some compatible resources
for i in R:
    for j in T:
        const3 = X[i][j]
        model += const3 <= A[i][j]

# 4). Each resources has the maximum number of tasks which can perform
for i in R:
    temp = []
    for j in T:
        temp.append((X[i][j], 1))
    const4 = pl.LpAffineExpression(temp)
    model += const4 <= M[i]
####################################
# endregion

# region : solve the problem
####################################
solver = pl.CPLEX_CMD()
result = model.solve(solver)

if result == 1:
    print("Model is OK")
else:
    print("Try Again Modeling")

print("Objective function: ", objective_function)
print("Objective function value: ",pl.value(model.objective))
print("-------------------------------------------------------------")
for i in R:
    print("Deviation negative of Workload: ", pl.value(D_negative[i]))
    print("Deviation positive of Workload: ", pl.value(D_positive[i]))

for i in R:
    for j in T:
        print("X_" + str(i) + '_' + str(j) + ' = ' + str(pl.value(X[i][j])))
####################################
# endregion