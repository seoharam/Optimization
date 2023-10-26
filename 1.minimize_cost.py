import pulp as pl # This is for C_plex module # module is assemble with function

# sets = 집합
R = [0, 1, 2] # R = Resource
T = [0, 1, 2, 3] # T = Task

# parameters = 매개변수, 상수 값
# This is  Dimension 2 for expression table
A = [[1,1,1,1], [1,0,1,0], [0,1,1,1]] # A = allow
C = [[8,5,7,5], [6,4,5,6], [8,6,7,6]] # C = cost
N_max = [2,2,2] # N_max = maximum number of assignment

# variables = 변수 # i is row, j is column
X = []
for i in R:
    temp_list = [] # make a vacant list for 2 dimension 
    for j in T:
        temp_list.append(pl.LpVariable('x_' + str(i) + '_' + str(j), cat = pl.LpBinary)) # make a Linear problem variable in pulp, cat = category, LpBinary = 2진법
    X.append(temp_list) # add the variable in temp_list for real variable

# ===================================================================================================

# model = 목적함수의 목표를 담당하는 모델
model = pl.LpProblem('test_lp', pl.LpMinimize) # LpProblem = Linear Problem, LpMinimize = smallest

# ===================================================================================================

# objective function = 목적함수
objective = []
for i in R:
    for j in T:
        objective.append((X[i][j], C[i][j])) # the reason why use tuple is purpose for C_plex # This is Dimension 1

objective_function = pl.LpAffineExpression(objective) # LpAffineExpression = This function can times X and C in same tuple and plus other tuple
model += objective_function # insert to model for express objective_function

# ===================================================================================================

# constraints
# constraint 1: All the tasks should be performed by a resource only once
for j in T:
    const_left1 = []
    for i in R:
        const_left1.append((X[i][j], 1)) # X_ij, 1 is constant variable
    c1 = pl.LpAffineExpression(const_left1) == 1 # This function can times X and 1 in same tuple and plus other tuple. # == is meaning about constraint
    model += c1 # insert to model for express const_left1

# constraint 2: Each task has some compatible resources
for i in R:
    for j in T:
        model += X[i][j] <= A[i][j]
        
# constraint 3: Each resource has the maximum number of tasks which can perform
for i in R:
    const_left3 = []
    for j in T:
        const_left3.append((X[i][j], 1))
    c3 = pl.LpAffineExpression(const_left3) <= N_max[i]
    model += c3 # insert to model for express const_left3

# ===================================================================================================

# solve the problem
model.solve()

# print the solution
print("model_value is", pl.value(model.objective)) # value(model.objective) = 모델의 목적함수의 값 도출
print("-------------------------------")

for i in R: # 이는 위의 목적함수에서 무슨 변수가 선정되었는지 확인할 겸 보여주는 식
    for j in T:
        print("X" + '_' + str(i) + '_' + str(j) + '=' + str(pl.value(X[i][j]))) # value(X[i][j])는 해당 변수가 선정되었는지 아닌지를 도출