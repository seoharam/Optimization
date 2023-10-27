import pulp as pl 
from tqdm import tqdm
import math

# region : Problem set
####################################
# Length와 Breadth을 선정해서 Atlantic Trade Inc.'s 의 연간 profit을 최대화하는 문제
####################################
# endregion

# region : sets (about decision variable index)
####################################
# Dimension indexed by i
I = [0, 1]
####################################
# endregion

# region : parameters (about data that was inserted)
####################################
# Lower value about dimension i
L = [180, 28]
# Upper value about dimension i
U = [380, 58]
# Fuel consumptiuon efficiency of dimension i
E = [3, 2]
# Cargo capacity of dimension i
C = [50, 0]
# Base cargo capacity
B_C = 40000
# Base fuel consumptiojn efficiency
B_F = 1400
# Maximum draft
M_D = 13
# Maximum voyage number
M_V = 25
# Minimum of cargo capacity
M_C = 14000
# Increasing draft about dimension i
D = [0.015, 0.025]
# Operating expenditure per liter
O = 0.48
# Profit per ton
P = 45
# Specific km
A = 10
####################################
# endregion

# region : decision variables (about answer we have to know for solving linear problem)
####################################
X = []
for i in I:
    X.append(pl.LpVariable('x_' + str(i), cat = pl.LpContinuous))
####################################
# endregion

# region : model (about Purpose in problem)
####################################
model = pl.LpProblem('Maximize_net_profits', pl.LpMaximize)
####################################
# endregion

# region : objective function (about function to solve this problem)
####################################
objective_1 = [] 
objective_2 = []
for index in I:
    objective_1.append((X[i], P*C[i]))
    objective_2.append((X[i], O*E[i]))
objective_function = P*B_C + pl.LpAffineExpression(objective_1) - O*A*B_F - pl.LpAffineExpression(objective_2)
model += objective_function 
####################################
# endregion

# region : constraints (about condition of decision variable)
####################################
# 1). constraint : dimension i value is between lower value and upper value
for i in I:
    const1 = L[i] <= X[i]
    const1_1 = X[i] <= U[i]
    model += const1
    model += const1_1
    
# 2). constraint : draft have upper limit
temp = []
for i in I:
    temp.append((X[i], D[i]))
const2 = pl.LpAffineExpression(temp)
model += const2 <= M_D

# 3). constraint : Cargo capacity have lower limit
temp = []
for i in I:
    temp.append((X[i], C[i]))
const3 = pl.LpAffineExpression(temp) + B_C
model += const3 >= M_C
####################################
# endregion

# region : solve the problem
####################################
solver = pl.CPLEX_CMD()
result = model.solve(solver)

print('Result : ', result) # 1 is ok in Cplex

# print the solution
print("model_value :", pl.value(model.objective)) # value(model.objective) = 모델의 목적함수의 값 도출
print("-------------------------------")
for i in I:
    print(f"X [{i}] : {pl.value(X[i])}")
####################################
# endregion