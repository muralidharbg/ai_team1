import cvxpy
from graph import Graph
import features_calc_training as calF
import random

#Node positions
my_nodes = {1: [1,1], 2: [2,2], 3: [4,4], 4: [6,6], 5: [7,8], 6: [1,9],
            7: [0,7], 8: [2,6], 9: [8,7], 10:[10,6]}

#The structure of the grand truth for this configuration
node_list = [1,2,3,4,5,6,7,8,9,10]

#Number of random graphs for training
num_random_graphs = 100

#Creating random graphs for training the weights
def create_rand_graphs():
    rand_nodes = []
    for i in range(num_random_graphs):
        rand_nodes.append(node_list.copy())

    for i in range(num_random_graphs):
        random.shuffle(rand_nodes[i])
    rand_nodes[0] = [1,3,2,4,5,6,7,8,9,10] 

    graph_list = []
    for i in range(num_random_graphs):
        temp_graph = []
        for j in range(len(rand_nodes[i])):
            temp_graph.append(my_nodes[rand_nodes[i][j]])
        graph_list.append(temp_graph)

    return rand_nodes,graph_list

#Calculating the features
def cal_features(graph_list):
    v_features_list = []
    e_features_list = []
    for i in range(num_random_graphs):
        V, E = calF.calcFeatures(graph_list[i])

        v_features_list.append(V)
        e_features_list.append(E)
    
    return v_features_list, e_features_list

#calculating the loss fucntion
def cal_distance(rand_nodes, orig_graph):
    distance_list = []
    for i in range(num_random_graphs):
        labelGraph = Graph();
        labelGraph.initializeADummyGraph( rand_nodes[i] )
        my_loss = labelGraph.getLossFunction( orig_graph ) 
        distance_list.append(my_loss)

    return distance_list

#Calculating the average of features for each graph configuration
def cal_mean_features(features_list, num_features):
    mean_features = []
    for i in range(len(features_list)):
        total_features = [0] * num_features
        for j in range(len(features_list[i])):
            for k in range(len(total_features)):
                total_features[k] = total_features[k] + features_list[i][j][k]
        average_f = [item / len(features_list[i]) for item in total_features]
        mean_features.append(average_f)  
    return mean_features

    
#Computes the weights for node features
#by solving the minimization formulation
def cal_V_Ws(Loss_values, V_features):
    
    d = 3   # Dimension of problem.
    w_v = cvxpy.Variable(d) #Weight vector
    xi_v = cvxpy.Variable() #Xi value

    #Objective 
    obj_cost = 0.5*cvxpy.sum_squares(w_v) + xi_v 
    obj = cvxpy.Minimize(obj_cost)

    #Defining the constraints
    constraints = []
    for i in range(len(Loss_values)):
        constraints += [w_v.T*V_features[i] >= Loss_values[i] - xi_v] 
    
    #Defining and solving the problem
    prob = cvxpy.Problem(obj, constraints)
    prob.solve()
    
    
    print("Problem Status: %s"%prob.status)
    w_v = w_v.value

    scores_v = []
    for i in range(num_random_graphs):
        score = w_v[0]*V_features[i][0] + w_v[1]*V_features[i][1] + w_v[2]*V_features[i][2]
        scores_v.append(score)

    return w_v, scores_v

#Computes the weights for vector features
#by solving the minimization formulation
def cal_E_Ws(Loss_values, E_features):
    
    d = 4   # Dimension of problem.
    w_e = cvxpy.Variable(d) #Weight vector
    xi_e = cvxpy.Variable() #Xi value

    obj_cost = 0.5*cvxpy.sum_squares(w_e) + xi_e
    obj = cvxpy.Minimize(obj_cost)

    constraints = []
    for i in range(len(Loss_values)):
        constraints += [w_e.T*E_features[i] >= Loss_values[i] - xi_e]
    

    prob = cvxpy.Problem(obj, constraints)

    prob.solve()
    print("Problem Status: %s"%prob.status)
    w_e = w_e.value
    
    scores_e = []
    for i in range(num_random_graphs):
        score = w_e[0]*E_features[i][0] + w_e[1]*E_features[i][1] + w_e[2]*E_features[i][2] + w_e[2]*mean_e_features[i][2]
        scores_e.append(score)

    return w_e, scores_e


#Creating the original graph
orig_graph = Graph();
orig_graph.initializeADummyGraph(node_list)

#Creating random node list and their respective graphs
rand_nodes, graph_list = create_rand_graphs()

#CAlcualting the features for the random lists
v_features_list, e_features_list = cal_features(graph_list)

#Clacualting the mean of features for each graph
#We are assigning one set of weights to each configuration
mean_v_features  = cal_mean_features(v_features_list, 3)
mean_e_features = cal_mean_features(e_features_list, 4)

#Calcualting the loss function for each random graph
distance_list = cal_distance(rand_nodes, orig_graph)

#Calcualting the weight list and the scores of each graph
w_v, scores_v = cal_V_Ws(distance_list, mean_v_features)
w_e, scores_e = cal_E_Ws(distance_list, mean_e_features)


