import pulp as pl 
from tqdm import tqdm
import math

# region : Problem set
####################################
# Module 단위의 설계를 할 때 Lifting capacity와 Ship speed의 Goal 값을 만족하면서, Cost를 일정 수준 이하로 낮추는 문제 
####################################
# endregion

# region : sets (about decision variable index)
####################################
# crane module indexed by i
I = [0,1,2]
# engine module indexed by j
J = [0,1,2]
####################################
# endregion

# region : parameters (about data that was inserted)
####################################
# Performance of crane module i
P_C = [20, 50, 100]
# Performnace of engine module j
P_E = [20, 30, 40]
# Aquisition cost of crane module i
C_C = [2, 4.5, 8]
# Aquisition cost of engine module j
C_E = [3, 5.5, 9]
# Goal value of Lifting capacity
G_L = 70
# Goal value of Ship speed
G_S = 30
# Max value of total modular acquisition cost
M_C = 12
####################################
# endregion

# region : decision variables (about answer we have to know for solving linear problem)
####################################
X = []
Y = []

for i in I:
    X.append(pl.LpVariable('X_' + str(i), cat=pl.LpBinary))
for j in J:
    Y.append(pl.LpVariable('Y_' + str(j), cat=pl.LpBinary))
    
D_positive_lift = pl.LpVariable('d_positive_lifting', lowBound = 0, upBound = None, cat = pl.LpContinuous)
D_negative_lift = pl.LpVariable('d_negative_lifting', lowBound = 0, upBound = None, cat = pl.LpContinuous)
D_positive_speed = pl.LpVariable('d_positive_speed', lowBound = 0, upBound = None, cat = pl.LpContinuous)
D_negative_speed = pl.LpVariable('d_negative_speed', lowBound = 0, upBound = None, cat = pl.LpContinuous)
####################################
# endregion

# region : model (about Purpose in problem)
####################################
model = pl.LpProblem('Goal_Problem', pl.LpMinimize)
####################################
# endregion

# region : objective function (about function to solve this problem)
####################################
objective_function = D_negative_lift + D_positive_lift + D_negative_speed + D_positive_speed
model += objective_function
####################################
# endregion

# region : constraints (about condition of decision variable)
####################################
# 1). constraint: Make relationship X and D_lift and G_L
temp = []
for i in I:
    temp.append((X[i], P_C[i]))
const1 = pl.LpAffineExpression(temp) + D_negative_lift - D_positive_lift
model += const1 == G_L

# 2). constraint: Make relationship Y and D_speed and G_S
temp = []
for j in J:
    temp.append((Y[j], P_E[j]))
const2 = pl.LpAffineExpression(temp) + D_negative_speed - D_positive_speed
model += const2 == G_S

# 3). constraint: Total cost of Acquisition cost have upper cost limit
temp1 = []
for i in I:
    temp1.append((X[i], C_C[i]))
temp2 = []
for j in J:
    temp2.append((Y[j], C_E[j]))
const3 = pl.LpAffineExpression(temp1) + pl.LpAffineExpression(temp2)
model += const3 <= M_C

# 4). constraint: Crane module is selected only one
temp = []
for i in I:
    temp.append((X[i], 1))
const4 = pl.LpAffineExpression(temp)
model += const4 == 1

# 5). constraint: Engine module is selected only one
temp = []
for j in J:
    temp.append((Y[j], 1))
const5 = pl.LpAffineExpression(temp)
model += const5 == 1
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
print("Deviation negative of Lifting_Capacity: ", pl.value(D_negative_lift))
print("Deviation positive of Lifting_Capacity: ", pl.value(D_positive_lift))
print("Deviation negative of Ship_speed: ", pl.value(D_negative_speed))
print("Deviation positive of Ship_speed: ", pl.value(D_positive_speed))

for i in I:
    print("X_" + str(i) + ' = ' + str(pl.value(X[i])))
for j in J:
    print("Y_" + str(j) + ' = ' + str(pl.value(Y[j])))
####################################
# endregion