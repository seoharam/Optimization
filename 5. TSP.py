import pulp as pl # pulp is a cplex module # module is assemble with functions
import math # for math calculation
import numpy as np # for math and science

# ============================================================================
# 목적: 부분적 순환 문제를 해결하기 위해 문제가 될 수 있는 부분집합
# parameter 설명: 주어진 N집합에서의 조건에 맞는 부분 집합을 뽑아내는 함수 설정이다
# ============================================================================

def get_subset(N, min_size, max_size): # N은 원래 집합, min_size는 부분 집합의 최소 사이즈, max_size는 부분 집합의 최대 사이즈, subset is 부분집합
    max_number = int(math.pow(2, len(N))) # math.pow(i,j)은 j의 i제곱, 부분집합 개수 = 2^n (본인 제외시 -1)
    S = [] # N의 부분집합 리스트
    for number in range(max_number): # 0부터 max_number-1 까지 number을 불러옴
        binary_list = list(bin(number)[2:]) # number 숫자를 2진수로 바꾸어 binary
        s = [] # 현재 number로 만들어지는 부분 집합에 들어갈 list s
        count = 0
        for i in range(len(binary_list)): # binary_list의 개수까지 i에 값을 대입 반복
            j = len(binary_list) - 1 - i # 숫자가 역순으로 생성, range에서는 끝 숫자에 -1이 붙어서 안넣어준 부분을 여기에 넣음
            # ---------------------------------------------------------------------
            if binary_list[i] == '1':
                s.append(N[-1-j]) # N 집합에서 역순으로 값을 불러와 넣음
                count += 1
            # ---------------------------------------------------------------------
        if min_size <= count and count <= max_size:
            S.append(s)
    return S

# set

N = [0, 1, 2, 3, 4] # 노드 집합 N
S = get_subset(N, 2, len(N)-2) # 조건(2 <= S <= N-2)에 맞는 부분집합의 set

# parameter

C = np.array([[1000, 5, 8, 2, 5],
              [5, 1000, 3, 6, 4],
              [7, 2, 1000, 3, 3],
              [3, 5, 2, 1000, 2],
              [4, 3, 2, 1, 1000]]) # 1000은 애초에 선택이 안되도록 유도한다. 목적은 Cost minimize니깐 알아서 선택 X

# decision variable define

X = []
for i in N:
    temp = []
    for j in N:
        temp.append(pl.LpVariable('x_' + str(i) + '_' + str(j), cat = pl.LpBinary))
    X.append(temp)
    
# model

model = pl.LpProblem("TSP", pl.LpMinimize)

# object function define (object : 최소 비용으로 이동한다.)

objective = []
for i in N:
    for j in N:
        objective.append((X[i][j], C[i][j]))
objective_function = pl.LpAffineExpression(objective)
model += objective_function

# constraint condition

# 1. 모든 노드는 한번의 출발지가 된다. (i는 나가는 것, j는 들어오는 것)

for i in N:
    temp = []
    for j in N:
        if i != j:
            temp.append((X[i][j], 1))
    const_left1 = pl.LpAffineExpression(temp) == 1 # 튜플끼리 곱하고 리스트안 요소끼리 더하는 module
    model += const_left1

# 2. 모든 노드는 한번의 도착지가 된다.

for j in N:
    temp = []
    for i in N:
        if i != j:
            temp.append((X[i][j], 1))
    const_left2 = pl.LpAffineExpression(temp) == 1
    model += const_left2

# 3. 부분적 순환 제거 (반복문 3개 필요 about s, i, j) # '부분집합별 순환 오류 = 부분적 순환'

for s in S:
    temp = []
    for i in s:
        for j in s:
            if i != j: # 해당 부분이 문제가 되는 부분 !
                temp.append((X[i][j], 1))
    const_left3 = pl.LpAffineExpression(temp) <= len(s) - 1
    model += const_left3
    
# Solving Problem

solver = pl.CPLEX_CMD() # 함수들은 () 안에 별도의 인자가 없으면 생략하기도 한다.
result = model.solve(solver)
print()
print('Result: ', result) # 1 is OK in Cplex

for i in N:
    for j in N:
        if round(pl.value(X[i][j])) == 1:
            print(X[i][j].name + '=' + str(X[i][j].varValue)) # varValue = value of Variable
print('cost =' , pl.value(model.objective))
