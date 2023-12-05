import pulp as pl 
from tqdm import tqdm
import math

# region : Problem set
####################################
# milestone 및 시작 시간, 종료 시간, lag를 만족하는 문제
####################################
# endregion

# region : sets (about decision variable index)
####################################
# Tasks indexed by i or j
T = []
# Milestones indexed by i, j
T_M = []
# Relations, indexed by (i,j)
R_FS = []
R_FF = []
R_SS = []
R_SF = []
####################################
# endregion

# region : parameters (about data that was inserted)
####################################
# Minimum Transition time (lag) between task i and task j in a FS relation
MIN_TR_FS = []
# Minimum Transition time (lag) between task i and task j in a FF relation
MIN_TR_FF = []
# Minimum Transition time (lag) between task i and task j in a SS relation
MIN_TR_SS = []
# Minimum Transition time (lag) between task i and task j in a SF relation
MIN_TR_SF = []
# Maximum Transition time (lag) between task i and task j in a FS relation
MAX_TR_FS = []
# Maximum Transition time (lag) between task i and task j in a FF relation
MAX_TR_FF = []
# Maximum Transition time (lag) between task i and task j in a SS relation
MAX_TR_SS = []
# Maximum Transition time (lag) between task i and task j in a SF relation
MAX_TR_SF = []
# Working time (duration) of actdivity of task i
WT = []
# Goal start time of task i -> In milestone, start time == finish time == 1
G = []
####################################
# endregion

# region : decision variables (about answer we have to know for solving linear problem)
####################################
# Start time of task i
X = []
for i in T:
    X.append(pl.LpVariable('x_' + str(i), cat = pl.LpContinuous))

# Finish time of task i
Y = []
for i in T:
    X.append(pl.LpVariable('y_' + str(i), cat = pl.LpContinuous))
    
# Lastest finish time out of all tasks -> This is automatically calculated by latest Finish time
z = pl.LpVariable('z', cat = pl.LpContinuous)

# Positive deviation between goal value and time of task i
D_negative = []
D_positive = []
for i in T:
    D_negative.append(pl.LpVariable('d_negative_' + str(i), lowBound = 0, upBound = None, cat = pl.LpContinuous))
    D_positive.append(pl.LpVariable('d_positive_' + str(i), lowBound = 0, upBound = None, cat = pl.LpContinuous))
####################################
# endregion

# region : model (about Purpose in problem)
####################################
model = pl.LpProblem('GP_scheduling', pl.LpMinimize)
####################################
# endregion

# region : objective function (about function to solve this problem)
####################################
temp = []
for i in T_M:
    temp.append(D_negative[i], 1)
    temp.append(D_positive[i], 1)
objective_function = z + pl.LpAffineExpression(temp)
model += objective_function
####################################
# endregion

# region : constraints (about condition of decision variable)
####################################
# 1). constraint : Define the relation between y_i and z
for i in T:
    const1 = Y[i]
    model += const1 <= z

# 2). constraint : Working time constraint of task i 
for i in T:
    const2 = X[i] + WT[i]
    model += const2 == Y[i]
    
# 3-1). constraint : Precedence of constraint of the FS relation between task i and task j in min lag
for i,j in MIN_TR_FS:
    const3 = X[j] - Y[i]
    model += const3 >= MIN_TR_FS[i,j]

# 3-2). constraint : Precedence of constraint of the FF relation between task i and task j in min lag
for i,j in MIN_TR_FF:
    const4 = Y[j] - Y[i]
    model += const4 >= MIN_TR_FF[i,j]
    
# 3-3). constraint : Precedence of constraint of the SS relation between task i and task j in min lag
for i,j in MIN_TR_SS:
    const5 = X[j] - X[i]
    model += const5 >= MIN_TR_SS[i,j]

# 3-4). constraint : Precedence of constraint of the SF relation between task i and task j in min lag
for i,j in MIN_TR_SF:
    const6 = Y[j] - X[i]
    model += const6 >= MIN_TR_SF[i,j]
    
# 4-1). constraint : Precedence of constraint of the FS relation between task i and task j in max lag
for i,j in MAX_TR_FS:
    const7 = X[j] - Y[i]
    model += const7 <= MAX_TR_FS[i,j]

# 4-2). constraint : Precedence of constraint of the FF relation between task i and task j in max lag
for i,j in MAX_TR_FF:
    const8 = Y[j] - Y[i]
    model += const8 <= MAX_TR_FF[i,j]
    
# 4-3). constraint : Precedence of constraint of the SS relation between task i and task j in max lag
for i,j in MAX_TR_SS:
    const9 = X[j] - X[i]
    model += const9 <= MAX_TR_SS[i,j]

# 4-4). constraint : Precedence of constraint of the SF relation between task i and task j in max lag
for i,j in MAX_TR_SF:
    const10 = Y[j] - X[i]
    model += const10 <= MAX_TR_SF[i,j]
    
# 5). constraint : relation between deviation and x and with G
for i in T_M:
    const11 = X[i] + D_negative[i] - D_positive[i]
    model += const11 == G[i]
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