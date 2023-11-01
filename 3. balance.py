import pulp as pl # This is C_plex module for optimization # module is assemble with function
import numpy as np # for math calculation

# sets # ===================================================================================================

R = [0, 1, 2] # R = resource
T = [0, 1, 2, 3, 4] # T = Task

# parameters # ===================================================================================================

A = [[1, 1, 1, 1, 0], [1, 1, 0, 1, 1], [0, 1, 1, 1, 1]] # A = Allowance
L = [8, 5, 7, 8, 4] # L = Workload of tasks
N_max = [2, 2, 2] # N_max = Maximum number of assignment
G =  sum(L)/len(L)# G = Goal value

# decision variable # ===================================================================================================

X = []
for i in R:
    temp_list = []
    for j in T:
        temp_list.append(pl.LpVariable('x_' + str(i) + '_' + str(j), cat = pl.LpBinary)) # make a Linear problem variable # binary has only 0 or 1
    X.append(temp_list)

D_negative = [] # d는 goal value와 resource i 사이의 오차 값
D_positive = []
for i in R:
    D_negative.append(pl.LpVariable('d_negative_' + str(i), lowBound = 0, upBound = None, cat = pl.LpContinuous)) # Continuous is float number
    D_positive.append(pl.LpVariable('d_positive_' + str(i), lowBound = 0, upBound = None, cat = pl.LpContinuous))

# model # ===================================================================================================

model = pl.LpProblem('test_lp', pl.LpMinimize) # LpProblem = Linear Problem, LpMinimize = Smallest, 여기서는 오차를 최소화하는 것이 목적
    
# objective function # ===================================================================================================

objective = []
for i in R:
    objective.append((D_negative[i], 1))
    objective.append((D_positive[i], 1))
    
model += pl.LpAffineExpression(objective)

# constraint 1: Make a relationship between x and d and G # ===================================================================================================

for i in R:
    temp = [] # for 2 dimension making
    for j in T:
        temp.append((X[i][j], L[j]))
    temp.append((D_negative[i], 1)) # 음수는 더해주고,
    temp.append((D_positive[i], -1)) # 양수는 빼줘서 절댓값을 최대한 Goal에 가깝게 만든다.
    const1_left = pl.LpAffineExpression(temp) # LpAffineExpression is about x and +
    model += const1_left == G

# constraint 2: All the tasks should be performed by a resource only one # ===================================================================================================

for j in T:
    temp = []
    for i in R:
        temp.append((X[i][j], 1))
    const2_left = pl.LpAffineExpression(temp)
    model += const2_left == 1

# constraint 3: Each task has some compatible resources # ===================================================================================================

for i in R:
    for j in T:
        model += X[i][j] <= A[i][j]
        
# constraint 4: All the resources should be used at least once & less than the max number # ===================================================================================================

for i in R: 
    temp = []
    for j in T:
        temp.append((X[i][j], 1))
    const4_left = pl.LpAffineExpression(temp)
    model += const4_left <= N_max[i]

# decision variable에 대하여 이론에서는 따로 constraint를 부가 하였지만 여기서는 LpVariable의 cat = Binary를 통해 이진법을 정의하여 상관 X

# solve the problem # ===================================================================================================

model.solve()

# print the solution # ===================================================================================================

print("model value is",pl.value(model.objective))

for i in R: # about deviation's each value
    print("Resource"+ "_" + str(i) + '_negative =' + str(pl.value(D_negative[i])))
    print("Resource"+ "_" + str(i) + '_positive =' + str(pl.value(D_positive[i])))

for i in R: # deviation's sum are 5.3
    for j in T:
        print("X_" + str(i) + '_' + str(j) + '=' + str(pl.value(X[i][j])))
        
k=1