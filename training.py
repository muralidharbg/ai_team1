import cvxpy
#from cvxpy import *
from graph import Graph
import features_calc as calF
import random
my_nodes = {1: [1,1], 2: [2,2], 3: [4,4], 4: [6,6], 5: [7,8], 6: [1,9],
            7: [0,7], 8: [2,6], 9: [8,7], 10:[10,6]}

#my_nodes = {1: [175, 59], 2: [280, 110], 3: [379, 171], 4: [441, 258],
#           5: [432, 379], 6: [339, 453], 7: [233, 433], 8: [237, 312],
#           9: [305, 229], 10: [405, 178], 11: [550, 103]}

node_list = [1,2,3,4,5,6,7,8,9,10]#,11]

#Computes the weights for node features
#by solving the minimization formulation
def cal_V_Ws(Loss_values, V_features):
    
    d = 3   # Dimension of problem.
    w_v = cvxpy.Variable(d)
    xi_v = cvxpy.Variable()

    obj_cost = cvxpy.sum_squares(w_v) + 0.1*xi_v
    obj = cvxpy.Minimize(obj_cost )

    constraints = []
    for i in range(len(Loss_values)):
        constraints += [w_v.T*V_features[i] >= Loss_values[i] - xi_v] 
    
    prob = cvxpy.Problem(obj, constraints)

    prob.solve()
    print("Problem Status: %s"%prob.status)
    w_v = w_v.value

    scores_v = []
    for i in range(20):
        score = w_v[0]*V_features[i][0] + w_v[1]*V_features[i][1] + w_v[2]*V_features[i][2]
        scores_v.append(score)

    return w_v, scores_v

#Computes the weights for vector features
#by solving the minimization formulation
def cal_E_Ws(Loss_values, E_features):
    
    d = 4   # Dimension of problem.

    w_e = cvxpy.Variable(d)
    xi_e = cvxpy.Variable()

    obj_cost = cvxpy.sum_squares(w_e) + 0.1*xi_e
    obj = cvxpy.Minimize(obj_cost)

    constraints = []
    for i in range(len(Loss_values)):
        constraints += [w_e.T*E_features[i] >= Loss_values[i] - xi_e]
    

    prob = cvxpy.Problem(obj, constraints)

    prob.solve()
    print("Problem Status: %s"%prob.status)
    w_e = w_e.value
    
    scores_e = []
    for i in range(20):
        score = w_e[0]*E_features[i][0] + w_e[1]*E_features[i][1] + w_e[2]*E_features[i][2] + w_e[2]*mean_e_features[i][2]
        scores_e.append(score)

    return w_e, scores_e



orig_graph = Graph();
orig_graph.initializeADummyGraph(node_list)


rand_nodes = []
for i in range(20):
    rand_nodes.append(node_list.copy())

for i in range(20):
    random.shuffle(rand_nodes[i])
rand_nodes[0] = [1,2,3,4,5,6,7,8,9,10]#,11]
rand_nodes[1] = [1,10,9,8,7,6,5,4,3,2]

graph_list = []
for i in range(20):
    temp_graph = []
    for j in range(len(rand_nodes[i])):
        temp_graph.append(my_nodes[rand_nodes[i][j]])
    graph_list.append(temp_graph)
    



v_features_list = []
e_features_list = []

for i in range(20):
    V, E = calF.calcFeatures(graph_list[i])
    v_features_list.append(V)
    e_features_list.append(E)
    
distance_list = []
for i in range(20):
    labelGraph = Graph();
    labelGraph.initializeADummyGraph( rand_nodes[i] )
    my_loss = labelGraph.getLossFunction( orig_graph ) 
    distance_list.append(my_loss)
    

mean_v_features = []


for i in range(len(v_features_list)):
    v_total = [0,0,0]
    for j in range(len(v_features_list[i])):
        v_total[0] = v_total[0] + v_features_list[i][j][0]
        v_total[1] = v_total[1] + v_features_list[i][j][1]
        v_total[2] = v_total[2] + v_features_list[i][j][2]
    v_average = [item / len(v_features_list[i]) for item in v_total]
    mean_v_features.append(v_average)

mean_e_features = []
for i in range(len(e_features_list)):
    e_total = [0,0,0,0]
    for j in range(len(e_features_list[i])):
        e_total[0] = e_total[0] + e_features_list[i][j][0]
        e_total[1] = e_total[1] + e_features_list[i][j][1]
        e_total[2] = e_total[2] + e_features_list[i][j][2]
        e_total[3] = e_total[3] + e_features_list[i][j][3]
    e_average = [item / len(e_features_list[i]) for item in e_total]
    mean_e_features.append(e_average)


w_v, scores_v = cal_V_Ws(distance_list, mean_v_features)
w_e, scores_e = cal_E_Ws(distance_list, mean_e_features)


