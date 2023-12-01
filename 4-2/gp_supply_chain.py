import pulp as pl 
from tqdm import tqdm
import math

# region : Problem set
####################################
# 협력업체에 일을 할당할 때 긴급도 및 각 협력업체의 capacity를 고려하는 문제
####################################
# endregion

# region : sets (about decision variable index)
####################################
# Supplier(협력업체) indexed by i
S = [0,1,2]
# Tasks indexed by j
T = [0,1,2]
####################################
# endregion

# region : parameters (about data that was inserted)
####################################
# Workload of task j
W = [1,2,3]
# Goal workload of supplier i
G_W = [1,2,3]
# Urgent type of task j -> binary
U_U = [0,0,1]
# Semi-urgent type of task j -> binary
U_S = [0,1,0]
# Non-urgent type of task j -> binary
U_N = [1,0,0]
# Ratio of urgent type
R_U = 10
# Ratio of semi-urgent type
R_S = 20
# Ratio of non-urgent type
R_N = 70
####################################
# endregion

# region : decision variables (about answer we have to know for solving linear problem)
####################################
# 1 if supplier i performs j, 0 otherwise
X = []
for i in S:
    temp = []
    for j in T:
        temp.append(pl.LpVariable('x_' + str(i) + '_' + str(j), cat = pl.LpBinary))
    X.append(temp)

# deviation between goal workload and supplier i workload
D_W_negative = []
D_W_positive = []
for i in S:
    D_W_negative.append(pl.LpVariable('d_w_negative_' + str(i), lowBound = 0, upBound = None, cat = pl.LpContinuous))
    D_W_positive.append(pl.LpVariable('d_w_positive_' + str(i), lowBound = 0, upBound = None, cat = pl.LpContinuous))

# deviation between urgency total workload and supplier i total workload
D_U_negative = []
D_U_positive = []
for i in S:
    D_U_negative.append(pl.LpVariable('d_u_negative_' + str(i), lowBound = 0, upBound = None, cat = pl.LpContinuous))
    D_U_positive.append(pl.LpVariable('d_u_positive_' + str(i), lowBound = 0, upBound = None, cat = pl.LpContinuous))

# deviation between semi-urgency total workload and supplier i total workload
D_S_negative = []
D_S_positive = []
for i in S:
    D_S_negative.append(pl.LpVariable('d_s_negative_' + str(i), lowBound = 0, upBound = None, cat = pl.LpContinuous))
    D_S_positive.append(pl.LpVariable('d_s_positive_' + str(i), lowBound = 0, upBound = None, cat = pl.LpContinuous))

# deviation between non-urgency total workload and supplier i total workload
D_N_negative = []
D_N_positive = []
for i in S:
    D_N_negative.append(pl.LpVariable('d_n_negative_' + str(i), lowBound = 0, upBound = None, cat = pl.LpContinuous))
    D_N_positive.append(pl.LpVariable('d_n_positive_' + str(i), lowBound = 0, upBound = None, cat = pl.LpContinuous))
####################################
# endregion

# region : model (about Purpose in problem)
####################################
model = pl.LpProblem('GP_supply_chain', pl.LpMinimize)
####################################
# endregion

# region : objective function (about function to solve this problem)
####################################
temp = []
for i in S:
    temp.append((D_W_negative[i], 1))
    temp.append((D_W_positive[i], 1))
    temp.append((D_U_negative[i], 1))
    temp.append((D_U_positive[i], 1))
    temp.append((D_S_negative[i], 1))
    temp.append((D_S_positive[i], 1))
    temp.append((D_N_negative[i], 1))
    temp.append((D_N_positive[i], 1))

objective_function = pl.LpAffineExpression(temp)
model += objective_function 
####################################
# endregion

# region : constraints (about condition of decision variable)
####################################
# 1). constraint : summation of all task's workload is under goal workload G_W
for i in S:
    temp = []
    for j in T:
        temp.append((X[i][j], W[j]))
    const1 = pl.LpAffineExpression(temp) + D_W_negative[i] - D_W_positive[i]
    model += const1 == G_W[i]

# 2). constraint : summation of urgent tasks's workload is same with workloads of total workloads * R_U
for i in S:
    temp = []
    temp2 = []
    for j in T:
        temp.append((X[i][j], W[j]))
        temp2.append((X[i][j], W[j]))
    const2 = pl.LpAffineExpression(temp)*U_U[j] + D_U_negative[i] - D_U_positive[i]
    model += const2 == R_U * pl.LpAffineExpression(temp2)

# 3). constraint : summation of semi-urgent tasks's workload is same with workloads of total workloads * R_S
for i in S:
    temp = []
    temp2 = []
    for j in T:
        temp.append((X[i][j], W[j]))
        temp2.append((X[i][j], W[j]))
    const3 = pl.LpAffineExpression(temp) * U_S[j] + D_S_negative[i] - D_S_positive[i]
    model += const3 == R_S * pl.LpAffineExpression(temp2)
    
# 4). constraint : summation of non-urgent tasks's workload is same with workloads of total workloads * R_S
for i in S:
    temp = []
    temp2 = []
    for j in T:
        temp.append((X[i][j], W[j]))
        temp2.append((X[i][j], W[j]))
    const4 = pl.LpAffineExpression(temp) * U_N[j] + D_N_negative[i] - D_N_positive[i]
    model += const4 == R_N * pl.LpAffineExpression(temp2)
    
# 5). constraint : task j is must be selected by supplier i
for i in S:
    temp = []
    for j in T:
        temp.append((X[i][j], 1))
    const5 = pl.LpAffineExpression(temp)
    model += const5 == 1
    
# 6). constraint : Each supplier have production capacity as G_W
for i in S:
    temp = []
    for j in T:
        temp.append((X[i][j], W[j]))
    const6 = pl.LpAffineExpression(temp)
    model += const6 <= G_W[i]
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
for i in S:
    for j in T:
        print(f"X [{i}] : {pl.value(X[i][j])}")
####################################
# endregion