import pulp as pl 
from tqdm import tqdm
import math
import datetime

# region : Problem set
####################################
# L,B,T를 0.1씩 combination할 때 building cost를 최소화하는 문제
####################################
# endregion

# region : sets (about decision variable index)
####################################
# Hull combination
H = {}

length_list = []
breadth_list = []
draft_list = []

# L(Length), B(Breadth), T(draft)
initial_length = 65
initial_breadth = 15
initial_draft = 5

while initial_length <= 100:
    length_list.append(round(initial_length,2))
    initial_length += 0.1

while initial_breadth <= 23:
    breadth_list.append(round(initial_breadth,2))
    initial_breadth += 0.1
    
while initial_draft <= 8:
    draft_list.append(round(initial_draft,2))
    initial_draft += 0.1

total_combinations = len(length_list) * len(breadth_list) * len(draft_list)

# 인덱스를 0부터 total_combinations - 1까지 순차적으로 설정
print('make sets about L,B,T')
for index in tqdm(range(total_combinations)):
    length_index = index % len(length_list)
    breadth_index = (index // len(length_list)) % len(breadth_list)
    draft_index = (index // (len(length_list) * len(breadth_list))) % len(draft_list)
    
    H[str(index)] = {
        'length': length_list[length_index],
        'breadth': breadth_list[breadth_index],
        'draft': draft_list[draft_index]
    }
####################################
# endregion

# region : parameters (about data that was inserted)
####################################
# Draft of ith combination
D = []
# Initial GM of ith combination
GM = []
# Block Coefficient of ith combination
C_B = []
# Displacement of ith combination
D_P = []
# Dead weight of ith combination
DWT = []
# Deck area of ith combiation
A = []
# Building cost of ith combination 
C = []
# Obesity of ith combiation
O = []

# Minimum deadweight
min_dwt = 4000
# Minimum deckarea
min_deck_area = 900
# Velocity of ship
velocity = 15 / 1.944
# Maximum obesity
max_obesity = 0.15
# Minimum initial GM
min_initial_gm = 0.15

# 모든 조합에 따른 paramter 집합 생성
print('make parameters along L,B,T')
for key, value in tqdm(H.items()):
    length = float(value['length'])
    breadth = float(value['breadth'])
    draft = float(value['draft'])
    
    # 값 계산하기
    ith_draft = draft+1.6
    ith_breadth = 0.07*breadth
    ith_C_b = 0.7+1/8*math.atan(23-100*(velocity/math.sqrt(9.81*length))/4)
    ith_Displacement = 1.025*length*breadth*draft*ith_C_b
    ith_DWT = 503.8 + 0.3824 * ith_Displacement
    ith_Deck_area = 0.5465 * (length*breadth) + 39.8
    ith_Building_cost = 0.000402 * (ith_DWT * velocity) - 1.572
    ith_Obesity = ith_C_b * breadth / length
    
    # L,B,T 조합대로 parameter 넣기
    D.append(ith_draft)
    GM.append(ith_breadth)
    C_B.append(ith_C_b)
    D_P.append(ith_Displacement)
    DWT.append(ith_DWT)
    A.append(ith_Deck_area)
    C.append(ith_Building_cost)
    O.append(ith_Obesity)
####################################
# endregion

# region : decision variables (about answer we have to know for solving linear problem)
####################################
# variables = 변수
X = []
for key in H.keys():
    X.append(pl.LpVariable('x_' + str(key), cat = pl.LpBinary)) # make a Linear problem variable in pulp, cat = category, LpBinary = 2진법
####################################
# endregion

# region : model (about Purpose in problem)
####################################
# LpProblem = Linear Problem, LpMinimize = smallest
model = pl.LpProblem('Minimize_cost', pl.LpMinimize)
####################################
# endregion

# region : objective function (about function to solve this problem)
####################################
objective = []
for key in H.keys():
    objective.append((X[int(key)], C[int(key)]))

objective_function = pl.LpAffineExpression(objective)
model += objective_function 
####################################
# endregion

# region : constraints (about condition of decision variable)
####################################
# constraint 1: all decision variables summation equal 1
const1 = []
for key in H.keys():
    const1.append((X[int(key)], 1))
    # This function can times X and 1 in same tuple and plus other tuple.
c1 = pl.LpAffineExpression(const1) == 1
model += c1 # insert to model for express const_left1

# constraint 2: DWT is bigger than max_dwt
const2 = []
for key in H.keys():
    const2.append((X[int(key)], DWT[int(key)]))
c2 = pl.LpAffineExpression(const2) >= min_dwt+1
model += c2

# constraint 3: Deck Area is bigger than max_deck_area
const3 = []
for key in H.keys():
    const3.append((X[int(key)], A[int(key)]))
c3 = pl.LpAffineExpression(const3) >= min_deck_area+1
model += c3

# constraint 4: initial GM is bigger or same with min_initial_gm
const4 = []
for key in H.keys():
    const4.append((X[int(key)], GM[int(key)]))
c4 = pl.LpAffineExpression(const4) >= min_initial_gm
model += c4

# constraint 5: Obesity is smaller or same with 0.15
const5 = []
for key in H.keys():
    const5.append((X[int(key)], O[int(key)]))
c5 = pl.LpAffineExpression(const5) <= max_obesity
model += c5
####################################
# endregion

# region : solve the problem 
####################################
solver = pl.CPLEX_CMD()
result = model.solve(solver)

print('Result: ', result) # 1 is ok in Cplex

# print the solution
print("model_value is", pl.value(model.objective)) # value(model.objective) = 모델의 목적함수의 값 도출
print("-------------------------------")
for index in range(len(H)):
    if pl.value(X[index]) != 0:
        print(f'result : Lenght = {H[str(index)]["length"]}, Breadth = {H[str(index)]["breadth"]}, Draft = {H[str(index)]["draft"]}')
k=1
####################################
# endregion