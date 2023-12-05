import pulp as pl 
from tqdm import tqdm
import math

# region : Problem set
####################################
# pathplanning 문제
####################################
# endregion

# region : sets (about decision variable index)
####################################
# Nodes indexed by n
N = []
# Nodes associated with tasks, indexed by t
T = []
# Arcs indexed by (i,j)
A = []
# Pull-out arcs indexed by (i,j)
A_PO = []
# Pull-in arcs indexed by (i,j)
A_PI = []
# Deadhead arcs indexd by (i,j)
A_DH = []
####################################
# endregion

# region : parameters (about data that was inserted)
####################################
# Cost for the transition between node i to node j
C = []
####################################
# endregion

# region : decision variables (about answer we have to know for solving linear problem)
####################################
# 1 if arc (i,j) is selected, 0 otherwise
X = []
for i,j in A:
    X.append(pl.LpVariable('x_'+str(i)+'_'+str(j), cat=pl.LpBinary))
####################################
# endregion

# region : model (about Purpose in problem)
####################################
model = pl.LpProblem('Minimize_pathplanning', pl.LpMinimize)
####################################
# endregion

# region : objective function (about function to solve this problem)
####################################
temp = []
for i,j in A:
    temp.append((X[i][j], C[i][j]))
objective_function = pl.LpAffineExpression(temp)
model += objective_function
####################################
# endregion

# region : constraints (about condition of decision variable)
####################################
# 1). constraint : Source node have only one pull-out Edge
for i,j in A_PO:
    const1 = X[i][j]
    model += const1 == 1
    
# 2). constraint : Sink node have only one pull-in Edge
for i,j in A_PI:
    const2 = X[i][j]
    model += const2 == 1
    
# 3). constraint : Without source node and sink node, Each node has an equal number of comming and outting edges
temp = []
temp2 = []
for i1,j1 in set(A_DH | A_PO):
    for i2,j2 in set(A_DH | A_PI):
        # if j1 is same with j2, add to 
        if j1 == j2:
            temp.append((X[i1][j1],1))
            temp2.append((X[i2][j2],1))
        const3 = pl.LpAffineExpression(temp) == pl.LpAffineExpression(temp2)
        model += const3
####################################
# endregion

# region : solve the problem
####################################
solver = pl.CPLEX_CMD()
result = model.solve(solver)

print('Result : ', result) # 1 is ok in Cplex
print('Objective function : ', objective_function)

# print the solution
print("Model_value :", pl.value(model.objective)) # value(model.objective) = 모델의 목적함수의 값 도출
print("-------------------------------")
for i in T:
    print(f"X[{i}] : {pl.value(X[i])}")
####################################
# endregion