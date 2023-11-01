import pulp as pl 
from tqdm import tqdm
import math

# region : Problem set
####################################
# 2가지 종류의 Juice를 생산할 때 순수익을 최대화하는 문제
####################################
# endregion

# region : sets (about decision variable index)
####################################
# Juice type indexed by i
I = [0, 1]
####################################
# endregion

# region : parameters (about data that was inserted)
####################################
# Profit of Juice type i
P = [7, 9]
# Stock number of Apples
S_A = 100
# Stock number of Mangos
S_M = 50
# Stock number of Oranges
S_O = 90
# Stock number of Berries
S_B = 80
# Maximum number of total bottles
M_B = 60
# Number of apples for making Apple-Mango Juice
N_A = 2
# Number of mangos for making Apple-Mango Juice
N_M = 1
# Number of Oranges for making Orange-Berry Juice
N_O = 3
# Number of Berries for making Orange-Berry Juice
N_B = 2 
####################################
# endregion

# region : decision variables (about answer we have to know for solving linear problem)
####################################
# 0 : number of Apple-Mango Juice / 1 : number of Orange-Berry Juice
X = []
for i in I:
    X.append(pl.LpVariable('x_' + str(i), lowBound= 0, cat = pl.LpContinuous)) 
####################################
# endregion

# region : model (about Purpose in problem)
####################################
model = pl.LpProblem('Maximize_profit', pl.LpMaximize)
####################################
# endregion

# region : objective function (about function to solve this problem)
####################################
temp = []
for i in I:
    temp.append((X[i], P[i]))
objective_function = pl.LpAffineExpression(temp)
model += objective_function
####################################
# endregion

# region : constraints (about condition of decision variable)
####################################
# 1). constraint : total number of bottles is smaller than M_B
temp = []
for i in I:
    temp.append((X[i], 1))
const1 = pl.LpAffineExpression(temp)
model += const1 <= M_B

# 2). constraint : total number of apples for making Apple-Mango Juice is smaller than S_A
const2 = N_A*X[0]
model += const2 <= S_A

# 3). constraint : total number of mangos for making Apple-Mango Juice is smaller than S_M
const3 = N_M*X[0]
model += const3 <= S_M

# 4). constraint : total number of oranges for making Orange-Berry Juice is smaller than S_O
const4 = N_O*X[1]
model += const4 <= S_O

# 5). constraint : total number of berries for making Orange-Berry Juice is smaller than S_B
const5 = N_B*X[1]
model += const5 <= S_B
####################################
# endregion

# region : solve the problem
####################################
solver = pl.CPLEX_CMD()
result = model.solve(solver)

print('------------------------------------------------')
print('Result: ', result) # 1 is ok in Cplex, Others there is no solution..
print('Objective function: ', objective_function)
print("model value: ",pl.value(model.objective))
print('------------------------------------------------')
        
for i in I:
    print("X_" + str(i) + ' = ' + str(pl.value(X[i])))

k=1
####################################
# endregion