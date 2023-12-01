import pulp as pl # This is C_plex module # module is assemble with function

# sets, 원래는 1부터 써야 하지만 컴퓨터에서는 0부터 세기 때문에 이렇게 적음
R = [0, 1, 2] # resource
T = [0, 1, 2, 3] # task

# parameters
# This is  Dimension 2 for express the table
A = [[1,1,1,1], [1,0,1,0], [0,1,1,1]] # Allow
E = [[0.8,0.5,0.7,0.5], [0.6,0.4,0.5,0.6], [0.8,0.6,0.7,0.6]] # Efficiency
N_min = [1,1,1] # N_min = Minimum number of assignment

# variables = 의사결정변수, i is Resource, j is Task
X = []
for i in R:
    temp_list = [] # for 2 dimension
    for j in T:
        temp_list.append(pl.LpVariable('x_' + str(i) + '_' + str(j), cat = pl.LpBinary)) # make a Linear problem variable # binary has only 0 or 1
    X.append(temp_list)

# model = 풀고자 하는 문제
model = pl.LpProblem('test_lp', pl.LpMaximize) # LpProblem = Linear Problem, LpMaximize = largest

# ===================================================================================================

# objective function
objective = []
for i in R:
    for j in T:
        objective.append((X[i][j], E[i][j]))

objective_function = pl.LpAffineExpression(objective)
model += objective_function

# ===================================================================================================

# constraints
# constraint 1: All the tasks should be performed by a resource only one
for j in T:
    const_left1 = []
    for i in R:
        const_left1.append((X[i][j], 1))
    cl = pl.LpAffineExpression(const_left1) == 1
    model += cl

# constraint 2: Each task has some compatible resources
for i in R:
    for j in T:
        model += X[i][j] <= A[i][j]
        
# constraint 3: All the resources should be used at least once
for i in R:
    const_left3 = []
    for j in T:
        const_left3.append((X[i][j], 1))
    c3 = pl.LpAffineExpression(const_left3) >= N_min[i]
    model += c3

# Decision variable에 대한 제약 조건은 이론에서만 적어주고, 코드 상에서는 Binary로 알아서 적용

# ===================================================================================================

# solve the problem
model.solve()

# print the solution
print("model value is",pl.value(model.objective))

for i in R:
    for j in T:
        print("X" + "_" + str(i) + '_' + str(j) + '=' + str(pl.value(X[i][j])))