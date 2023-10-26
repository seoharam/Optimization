import pulp as pl # This is C_plex module # module is assemble with function
from math import sqrt
import numpy as np # for math calculation

# Eeconomy of Quantity

# set ---------------------------------------------------------------------

T = [] # Time steps indexed by t
for i in range (9): # 0 ~ 8
    T.append(i)

# parameter ---------------------------------------------------------------------

D = [35, 30, 42, 18, 20, 45, 35, 24, 30] # Demand quantity
L = 2 # Lead time, 발주 ~ 도착지점까지 시간
C_o = 50 # Order cost
C_i = 1.2 # Inventory holding cost
M = 1444 # for not selected

# decision variable define about X, Y, Z ---------------------------------------------------------------------

X = [] # order quantity at time step
for i in T:
    X.append(pl.LpVariable('x_' + str(i), lowBound = 0, cat = pl.LpInteger)) # integer is 정수

# X = [pl.LpVariable('x_' + str(i), lowBound = 0, cat = pl.LpInteger) for i in T] # 이는 바로 리스트에 넣는 코드

Y = [] # yes or no
for i in T:
    Y.append(pl.LpVariable('Y_' + str(i), cat = pl.LpBinary)) # 이진수라서 lowBound = 0, upBound = 1 이 정보 필요 없다.
    
Z = [] # inventory quantity at time step
for i in T:
    Z.append(pl.LpVariable('Z_' + str(i), cat = pl.LpInteger)) # X와 다르게 lowBound가 없어서 음의 정수도 가능하다. 현실 세계에서는 재고가 (-)도 가능하다.


# model ---------------------------------------------------------------------

model = pl.LpProblem("EOQ", pl.LpMinimize) # economic cost is equal minimum cost

# objective function define (object : 재고유지비용 + 주문비용 최소화.) ---------------------------------------------------------------------

objective_terms1 = pl.LpAffineExpression([(Y[i], C_o) for i in T]) # LpAffineExpression은 튜플 안 요소를 곱하고 더한다.
objective_terms2 = pl.LpAffineExpression([(Z[i], C_i) for i in T])
model += objective_terms1 + objective_terms2 # 부등호가 없으면 목적함수이고 아니면 제약함수라고 판단이 가능하다.

# constraint condition ---------------------------------------------------------------------

# 1. 재고량은 항상 0이상을 유지한다.

for t in T:
    model += Z[t] >= 0 # decision variable에서는 모든 정수로 지정했지만 이상적인 값은 항상 0 이상인 것이다.

# 2. 재고량(Z_t), 수요(D_t), 주문량(X_t)의 관계를 결정하는 식

for t in range(L,len(T)): # t의 범위는 L(리드 타임)부터 시작
    constleft1 = Z[t] - Z[t-1] - X[t-L]
    model += constleft1 == -D[t]
    
# 3. 주문량과 주문여부 의사결정변수의 관계식을 결정하는 식

for t in T:
    model += X[t] <= M * Y[t] # 주문을 하면 주문량이 있고, 주문을 하지 않으면 주문량이 없다.
    
# 4. X[0]와 X[1], Z[0]과 Z[1]의 값을 고정, 이미 결정되어 있기 때문에

model += X[0] == 0
model += X[1] == 0
model += Z[0] == 110
model += Z[1] == 80

# Solving Problem ---------------------------------------------------------------------

solver = pl.CPLEX_CMD()
result = model.solve(solver)
print()
print('Result: ', result) # 1 is ok in Cplex

for t in T:
    print('{}일 주문량: {}'.format(t, pl.value(X[t])))
    print('{}일 주문여부: {}'.format(t, pl.value(Y[t])))
    print('{}일 재고량: {}'.format(t, pl.value(Z[t])))
    print('===================')

print('cost = ' , model.objective)
print('cost = ',  pl.value(model.objective))