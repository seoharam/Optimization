import pulp as pl 
from tqdm import tqdm
import math

# region : Problem set
####################################
# 시작 시간, 종료 시간을 만족하며 전체 완료 시간을 줄이는 문제
####################################
# endregion

# region : sets (about decision variable index)
####################################
# Tasks indexed by i or j
T = []
# Relations, indexed by (i,j)
R_FS = []
R_FF = []
R_SS = []
R_SF = []
####################################
# endregion

# region : parameters (about data that was inserted)
####################################
# Transition time (lag) between task i and task j in a FS relation
TR_FS = []
# Transition time (lag) between task i and task j in a FF relation
TR_FF = []
# Transition time (lag) between task i and task j in a SS relation
TR_SS = []
# Transition time (lag) between task i and task j in a SF relation
TR_SF = []
# Working time (duration) of actdivity of task i
WT = []
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
####################################
# endregion

# region : model (about Purpose in problem)
####################################
model = pl.LpProblem('Minimize_completion_time', pl.LpMinimize)
####################################
# endregion

# region : objective function (about function to solve this problem)
####################################
objective_function = z
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
    model += const2 <= Y[i]
    
# 3). constraint : Precedence of constraint of the FS relation between task i and task j
for i,j in TR_FS:
    const3 = Y[i] + TR_FS[i,j]
    model += const3 <= X[j]

# 4). constraint : Precedence of constraint of the FF relation between task i and task j
for i,j in TR_FF:
    const4 = Y[i] + TR_FF[i,j]
    model += const4 <= Y[j]
    
# 5). constraint : Precedence of constraint of the SS relation between task i and task j
for i,j in TR_SS:
    const5 = X[i] + TR_SS[i,j]
    model += const5 <= X[j]

# 6). constraint : Precedence of constraint of the SF relation between task i and task j
for i,j in TR_SF:
    const6 = X[i] + TR_SF[i,j]
    model += const6 <= Y[j]
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