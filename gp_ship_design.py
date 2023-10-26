import pulp as pl 
from tqdm import tqdm
import math

# region : Problem set
####################################
# 모듈 단위의 설계를 할 때 lifting capacity와 ship speed의 goal 값을 맞추면서, 최대 비용을 넘지 않도록 만족하는 최적 모듈 선택
####################################
# endregion

# region : sets (about decision variable index)
####################################
# I : Crane modules indexed by i / J : Engine modules indexed by j
I = [0,1,2]
J = [0,1,2]
####################################
# endregion

# region : parameters (about data that was inserted)
####################################
# Lifting capacity of crane module i
P_L = [20, 50, 100]
# Aquisition cost of crane module i
C_C = [2, 4.5, 8]
# Ship speed of engine module j
P_S = [20, 30, 40]
# Aquisition cost of engine module j
C_E = [3, 5.5, 9]
# Goal value of lifting capacity (tons)
G_L = 70
# Goal value of ship speed (knots)
G_S = 30
# Maximum aquisition cost (million $)
M_C = 12
####################################
# endregion

# region : decision variables (about answer we have to know for solving linear problem)
####################################
# 1 if crane module i is selected, Otherwise 0
X = []
for i in I:
    # make a Linear problem variable in pulp, cat = category, LpBinary = 이진수
    X.append(pl.LpVariable('x_' + str(i), cat = pl.LpBinary)) 

# 1 if engine module j is selected, Otherwise 0
Y = []
for i in J:
    # make a Linear problem variable in pulp, cat = category, LpBinary = 이진수
    Y.append(pl.LpVariable('y_' + str(i), cat = pl.LpBinary))

# Deviation of lifting capacity
#  ㄴ 모든 resource와 task를 사용할 때는 그에 맞는 모든 deviation이 필요하지만, 지금은 단일 모듈만 사용하기 때문에 index가 필요가 없다.
D_negative_lift = [] 
D_positive_lift = []

D_negative_lift.append(pl.LpVariable('d_negative_lift', lowBound = 0, upBound = None, cat = pl.LpContinuous))
D_positive_lift.append(pl.LpVariable('d_positive_lift', lowBound = 0, upBound = None, cat = pl.LpContinuous))
    
# Deviation of ship speed
D_negative_speed = [] 
D_positive_speed = []

D_negative_speed.append(pl.LpVariable('d_negative_speed', lowBound = 0, upBound = None, cat = pl.LpContinuous))
D_positive_speed.append(pl.LpVariable('d_positive_speed', lowBound = 0, upBound = None, cat = pl.LpContinuous))
####################################
# endregion

# region : model (about Purpose in problem)
####################################
model = pl.LpProblem('Goal_Programming', pl.LpMinimize)
####################################
# endregion

# region : objective function (about function to solve this problem)
####################################
objective_function = D_positive_lift[0] + D_negative_lift[0] +  D_positive_speed[0] + D_negative_speed[0]

# This function can times function and 1 in same tuple and plus other tuple. like sigma
model += objective_function
####################################
# endregion

# region : constraints (about condition of decision variable)
####################################
# 1). Make a relationship between x and d_lift and G_L
temp = []
for i in I:
    temp.append((X[i], P_L[i]))
const1_left = pl.LpAffineExpression(temp) + D_negative_lift[0] - D_positive_lift[0]
model += const1_left == G_L
    
# 2). Make a relationship between y and d_speed and G_S
temp = []
for j in J:
    temp.append((Y[j], P_S[j]))
const2_left = pl.LpAffineExpression(temp) + D_negative_speed[0] - D_positive_speed[0]
model += const2_left == G_S

# 3). Total Aquisition cost must smaller than M_C
temp_c = []
temp_e = []
for i in  I:
    temp_c.append((X[i], C_C[i]))
    
for j in J:
    temp_e.append((Y[j], C_E[j]))
const3_left = pl.LpAffineExpression(temp_c) + pl.LpAffineExpression(temp_e)
model += const3_left <= M_C
    
# 4). decision variable x is selected only one
temp =[]
for i in I:
    temp.append((X[i], 1))

const4_left = pl.LpAffineExpression(temp)
model += const4_left == 1

# 5). decision variable y is selected only one
temp =[]
for j in J:
    temp.append((Y[j],1))
const5_left = pl.LpAffineExpression(temp)
model += const5_left == 1
####################################
# endregion

# region : solve the problem
####################################
solver = pl.CPLEX_CMD()
result = model.solve(solver)

print('Result: ', result) # 1 is ok in Cplex

print("model value is",pl.value(model.objective))

for i in I:
    print("Crane"+ "_" + str(i) + '_negative = ' + str(pl.value(D_negative_lift[0])))
    print("Crane"+ "_" + str(i) + '_positive = ' + str(pl.value(D_positive_lift[0])))

for j in J:
    print("Engine"+ "_" + str(j) + '_negative = ' + str(pl.value(D_negative_speed[0])))
    print("Engine"+ "_" + str(j) + '_positive = ' + str(pl.value(D_positive_speed[0])))
        
for i in I:
    print("X_" + str(i) + ' = ' + str(pl.value(X[i])))
    
for j in J:
    print("Y_" + str(j) + ' = ' + str(pl.value(Y[j])))
    
print(objective_function)
####################################
# endregion