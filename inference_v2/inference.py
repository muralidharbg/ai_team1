import collections
import numpy as np
import matplotlib.pyplot as plt
from features_calc_numbers import getGraph
from random import randint
import sys
import random

vertex = [[1,1],[2,2],[2,5],[2,7],[3,3],[3,8],[4,2],[4,4],[4,7],[5,1],[5,5],[5,6]]
# vertex = [[1,1],[2,2],[3,3],[4,4],[5,5],[5,6],[4,7],[3,8],[2,7],[2,5],[3,3],[4,2],[5,1]]
weights = {
	"V": [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
	"E": [[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
}
# features = {
# 	"V": [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
# 	"E": [[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
# }

def calculate_vertex_score(vertex_feature):
	value = k = 0
	for k in range(3):
		value += 1 * vertex_feature[k]
	
	return value

def all_vertex_score(features):
	vertex_score = []
	try:
		for graph_feature in range(len(features)):
			
			graph_vertex_score = []
			for i in range(len(features[graph_feature]["V"])):
				graph_vertex_score.append(calculate_vertex_score(features[graph_feature]["V"][i]))
			vertex_score.append(graph_vertex_score)

	except Exception as e:
		print("Error calculating vertex score.", e)
	finally:
		return vertex_score

def calculate_edge_score(edge_feature):
	value = k = 0
	for k in range(4):
		value += 1 * edge_feature[k]
	
	return value

def all_edge_score(features):
	edge_score = []
	try:
		for graph_feature in range(len(features)):
			graph_edge_score = []
			for i in range(len(features[graph_feature]["E"])):
				graph_edge_score.append(calculate_edge_score(features[graph_feature]["E"][i]))

			edge_score.append(graph_edge_score)

	except Exception as e:
		print("Error calculating edge score.", e)
	finally:
		return edge_score

# need to change
def vertex_edge_map(vertex_pairs_list):
	j = 0
	vertex_edge_map = []
	for graph in vertex_pairs_list:
		temp = collections.OrderedDict()
		for i in range(len(graph)):
			temp[tuple(graph[i])] = j
			j += 1
		vertex_edge_map.append(temp)
	
	return vertex_edge_map

def scatter(vertex):
	# data = np.concatenate(vertex, axis = 0)
	data = np.array(vertex)
	x, y = data.T

	plt.scatter(x,y)
	
def plot(vertex_edge_map, vertex):
	scatter(vertex)
	for graph in range(len(vertex_edge_map)):
		for vertex_pair, edge in vertex_edge_map[graph].items():
			vertex1, vertex2 = vertex_pair
			x = [vertex[vertex1][0],vertex[vertex2][0]]
			y = [vertex[vertex1][1],vertex[vertex2][1]]
			plt.plot(x,y,'-o')

def degree_of_vertices(vertex_edge_map, vertex_size):
	vertex_degree = np.zeros(vertex_size+1,dtype=int)
	for vertex_pair in vertex_edge_map.keys():
		vertex1, vertex2 = vertex_pair
		vertex_degree[vertex1] = vertex_degree[vertex1] + 1
		vertex_degree[vertex2] = vertex_degree[vertex2] + 1

	return vertex_degree

def regraph(vertex_edge_map, old_vertex_list):
	new_vertex = []

	for vertex_pair in vertex_edge_map.keys():
		vertex1, vertex2 = vertex_pair
		new_vertex.append(old_vertex_list[vertex1])

	new_vertex.append(old_vertex_list[vertex2])
	return new_vertex

def move1(vertex_edge_map, vertex_score, edge_score, graph_list):
	"""
	1. Find score of segments (two adjacent vertices with a connecting edge)
	2. Find lowest score segment and remove the edge connecting them and split the graph into sub graphs 
	"""
	all_segement_score = []
	min_segment_graph_list = []
	
	for graph in range(len(vertex_edge_map)):
		graph_segement_score = collections.OrderedDict()
		for vertex_pair, edge in vertex_edge_map[graph].items():
			vertex1, vertex2 = vertex_pair
			segment_score = vertex_score[graph][vertex1] + vertex_score[graph][vertex2] + edge_score[graph][edge]
			graph_segement_score[vertex_pair] = segment_score

		all_segement_score.append(graph_segement_score)
		min_segement = min(all_segement_score[graph], key=all_segement_score[graph].get)
		min_segment_graph_list.append(all_segement_score[graph][min_segement])

	min_segement_graph = np.argmin(min_segment_graph_list)
	min_segment_score = min_segment_graph_list[min_segement_graph]
	
	min_segement = min(all_segement_score[min_segement_graph], key=all_segement_score[graph].get)

	new_vertex_edge_map = list(vertex_edge_map)
	del new_vertex_edge_map[min_segement_graph][min_segement]
	# min_graph = graph_list[min_segement_graph]
	
	vertex_degree = degree_of_vertices(new_vertex_edge_map[min_segement_graph], len(vertex_score[min_segement_graph]))
	excluded_vertex, = np.where(vertex_degree == 0)
	
	# graph_list[min_segement_graph] = min_graph[:excluded_vertex[0]]
	
	# graph_list.append(min_graph[excluded_vertex[0]:])
	return new_vertex_edge_map, min_segement, graph_list

def move2(vertex_edge_map, removed_segement, graph_list, vertex_score):
	""" 1. Find a vertex with degree of zero (no connecting edges) in any subgraph,
	2. Connect it to any random vertex of a random subgraph such that it does not form the same segment removed in move1
	"""
	graph_vertex_degree = []
	for graph in range(len(vertex_edge_map)):
		graph_vertex_degree.append(degree_of_vertices(vertex_edge_map[graph], len(vertex_score[graph]))) 	

	min_degree = 0
	min_degree_graph = None
	for graph in range(len(graph_vertex_degree)):
		min_value = min(graph_vertex_degree[graph])
		if min_value <= min_degree:
			min_degree_graph = graph
			min_degree = min_value

	new_vertex_edge_map = list(vertex_edge_map)

	if min_degree_graph != None:
		subgraph_excluded_vertex, = np.where(graph_vertex_degree[min_degree_graph] == min_degree)
		excluded_vertex = graph_list[min_degree_graph][subgraph_excluded_vertex[0]] 
		
		while True:
			random_subgraph = np.random.choice(range(len(vertex_edge_map)),1)[0]
			if len(graph_list[random_subgraph]) > 1:
				random_vertex = np.random.choice(np.where(graph_vertex_degree[random_subgraph] > 0)[0],1)[0]
				if((excluded_vertex,random_vertex) != removed_segement and (random_vertex, excluded_vertex) != removed_segement):
					new_segment = (random_vertex,excluded_vertex)
					break 
			
		new_vertex_edge_map[random_subgraph].update({new_segment: next(reversed(new_vertex_edge_map[random_subgraph].values())) + 1})
		# graph_list[random_subgraph].append(excluded_vertex)
		# graph_list[min_degree_graph].remove(excluded_vertex)
		
		if len(new_vertex_edge_map[min_degree_graph]) == 0:
			# graph_list.pop(min_degree_graph)
			new_vertex_edge_map.pop(min_degree_graph)

		# print(random_vertex)

	# one_degree_vertex = np.argwhere(vertex_degree == 1)
	# for vertex_point in one_degree_vertex:
	# 	if((excluded_vertex[0][0],vertex_point[0]) != min_segement and (vertex_point[0], excluded_vertex[0][0]) != min_segement):
	# 		new_segment = (vertex_point[0],excluded_vertex[0][0])
	
	# print(vertex_edge_map_m1)
	return new_vertex_edge_map, graph_list 

def move4(vertex_edge_map, graph_list, vertex_score):
	""" 
	1. find two vertex with degree of 1 (which would be the end points in the graph) of any sub graph, 
	2. remove the edge connecting to the first one and connect it to the other edge   
	"""
	graph_vertex_degree = []
	for graph in range(len(vertex_edge_map)):
		graph_vertex_degree.append(degree_of_vertices(vertex_edge_map[graph], len(vertex_score[graph])))

	while True:
		rotate = False
		random_subgraph = np.random.choice(range(len(vertex_edge_map)),1)[0]
		if len(graph_list[random_subgraph]) > 1:
			subgraph_end_vertex, = np.where(graph_vertex_degree[random_subgraph] == 1)
			for vertex_pair in vertex_edge_map[random_subgraph].keys():
				if subgraph_end_vertex[0] in vertex_pair:
					del vertex_edge_map[random_subgraph][vertex_pair]
					vertex_edge_map[random_subgraph].update({(subgraph_end_vertex[1], subgraph_end_vertex[0]): next(reversed(vertex_edge_map[random_subgraph].values())) + 1})
					# graph_list[random_subgraph].remove(subgraph_end_vertex[0])
					# graph_list[random_subgraph].insert(graph_list[random_subgraph].index(subgraph_end_vertex[1]) + 1, subgraph_end_vertex[0])
					rotate = True
					break

		if rotate == True:
			break

	return vertex_edge_map, graph_list

def move5(vertex_edge_map, graph_list, vertex_score, edge_score):
	minscore = 100000
	min_first_vertex = first_vertex = min_second_vertex = common_vertex = min_third_vertex = third_vertex = None 
	for graph in range(len(vertex_edge_map)):
		for vertex_pair1, edge1 in vertex_edge_map[graph].items():
			vertex1, vertex2 = vertex_pair1
			for vertex_pair2, edge2 in vertex_edge_map[graph].items():
				# if (vertex1 in vertex_pair2) ^ (vertex2 in vertex_pair2):
					# third_vertex = vertex_pair2[0] if (vertex_pair2[0] != vertex1 and vertex_pair2[0] != vertex2) else vertex_pair2[1]
					# common_vertex = vertex1 if vertex1 in vertex_pair2 else vertex2
					# first_vertex = vertex1 if common_vertex != vertex1 else vertex2

				if (vertex2 in vertex_pair2) and (vertex_pair2 != vertex_pair1):
					third_vertex = vertex_pair2[0] if (vertex_pair2[0] != vertex2) else vertex_pair2[1]
					common_vertex = vertex2
					first_vertex = vertex1
					con_seg_score = vertex_score[graph][first_vertex] + vertex_score[graph][common_vertex] + edge_score[graph][edge1] + vertex_score[graph][third_vertex] + edge_score[graph][edge2]
					if con_seg_score < minscore:
						minscore = con_seg_score
						minpair1 = vertex_pair1
						minpair2 = vertex_pair2
						min_graph = graph
						min_first_vertex = first_vertex
						min_second_vertex = common_vertex
						min_third_vertex = third_vertex
	
	fourth_vertex = fourth_vertex_pair = None
	for vertex_pair in vertex_edge_map[min_graph].keys():
		if min_third_vertex in vertex_pair and vertex_pair != minpair1 and vertex_pair != minpair2:
			fourth_vertex = vertex_pair[0] if vertex_pair[0] != min_third_vertex else vertex_pair[1]
			fourth_vertex_pair = vertex_pair


	fifth_vertex = fifth_vertex_pair = None
	for vertex_pair in vertex_edge_map[min_graph].keys():
		if fourth_vertex in vertex_pair and vertex_pair != fourth_vertex_pair: 
			fifth_vertex = vertex_pair[0] if vertex_pair[0] != fourth_vertex else vertex_pair[1]
			fifth_vertex_pair = vertex_pair

	vertex_edge_map_keys = list(vertex_edge_map[min_graph].keys())
	vertex_edge_map_keys.remove(fourth_vertex_pair)
	vertex_edge_map_keys.insert(vertex_edge_map_keys.index(minpair1),(fourth_vertex,min_first_vertex))
	vertex_edge_map_keys.remove(fifth_vertex_pair)
	vertex_edge_map_keys.insert(vertex_edge_map_keys.index(minpair2)+1,(min_third_vertex,fifth_vertex))

	# print(vertex_edge_map_keys)

	new_vertex_edge_map = list(vertex_edge_map)
	new_vertex_pairs = list_of_vertex_pairs(new_vertex_edge_map)

	del new_vertex_pairs[min_graph]
	new_vertex_pairs.insert(min_graph, vertex_edge_map_keys)

	return new_vertex_pairs

def move6(vertex_edge_map):
	new_vertex_pairs = []

	random_subgraph = np.random.randint(low = 0, high = len(vertex_edge_map), size = 1)[0]
	if len(vertex_edge_map[random_subgraph]) > 1:
		start = length1 = len(vertex_edge_map[random_subgraph])/2
		while (start + length1) > len(vertex_edge_map[random_subgraph])/2:
			start = random.randint(1,((len(vertex_edge_map[random_subgraph]))/2))
			length1 = random.randint(2,4)
		start2 = random.randint(start+length1+2,len(vertex_edge_map[random_subgraph])-3)
		length2 = length1
		while (start2+length2) > len(vertex_edge_map[random_subgraph])-1:
			length2 = random.randint(2,(len(vertex_edge_map[random_subgraph])-1)/2)

		segment1 = []
		seg1_vertex_pair = vertex_edge_map[random_subgraph].keys()[start]
		segment1.append(seg1_vertex_pair)
		# segment1_vertex = list(seg1_vertex_pair)
		for vertex_pair in vertex_edge_map[random_subgraph].keys():
			if len(segment1) == length1:
				break

			if seg1_vertex_pair[1] in vertex_pair and vertex_pair not in segment1:
				segment1.append(vertex_pair)
				seg1_vertex_pair = vertex_pair

		seg1_vfirst = segment1[0][0]
		prev1_vertex_pair = None
		for vertex_pair in vertex_edge_map[random_subgraph].keys():
			if seg1_vfirst in vertex_pair and vertex_pair not in segment1:
				prev1_vertex_pair = vertex_pair

		next1_vertex_pair = None
		seg1_vend = segment1[len(segment1)-1][1]
		for vertex_pair in vertex_edge_map[random_subgraph].keys():
			if seg1_vend in vertex_pair and vertex_pair not in segment1:
				next1_vertex_pair = vertex_pair

		segment2 = []
		seg2_vertex_pair = vertex_edge_map[random_subgraph].keys()[start2]
		segment2.append(seg2_vertex_pair)
		
		for vertex_pair in vertex_edge_map[random_subgraph].keys():
			if len(segment2) == length2:
				break

			if seg2_vertex_pair[1] in vertex_pair and vertex_pair not in segment2:
				segment2.append(vertex_pair)
				seg2_vertex_pair = vertex_pair

		seg2_vfirst = segment2[0][0]
		prev2_vertex_pair = None
		for vertex_pair in vertex_edge_map[random_subgraph].keys():
			if seg2_vfirst in vertex_pair and vertex_pair not in segment2:
				prev2_vertex_pair = vertex_pair

		next2_vertex_pair = None
		seg2_vend = segment2[len(segment2)-1][1]
		for vertex_pair in vertex_edge_map[random_subgraph].keys():
			if seg2_vend in vertex_pair and vertex_pair not in segment2:
				next2_vertex_pair = vertex_pair

		if prev1_vertex_pair != None and next1_vertex_pair != None and prev2_vertex_pair != None and next2_vertex_pair != None:
			new_vertex_edge_map_keys = list(vertex_edge_map[random_subgraph].keys())
			
			prev1_vertex_pair_index = new_vertex_edge_map_keys.index(prev1_vertex_pair)

			prev1_vertex_pair = list(prev1_vertex_pair)
			prev1_vertex_pair[prev1_vertex_pair.index(seg1_vfirst)] = seg2_vfirst
			prev1_vertex_pair = tuple(prev1_vertex_pair)
			new_vertex_edge_map_keys[prev1_vertex_pair_index] = prev1_vertex_pair

			new_vertex_edge_map_keys = new_vertex_edge_map_keys[:prev1_vertex_pair_index+1] + segment2 + new_vertex_edge_map_keys[prev1_vertex_pair_index+1+length1:]
			
			next1_vertex_pair_index = new_vertex_edge_map_keys.index(next1_vertex_pair)
			next1_vertex_pair = list(next1_vertex_pair)
			next1_vertex_pair[next1_vertex_pair.index(seg1_vend)] = seg2_vend
			next1_vertex_pair = tuple(next1_vertex_pair)
			new_vertex_edge_map_keys[next1_vertex_pair_index] = next1_vertex_pair

			prev2_vertex_pair_index = new_vertex_edge_map_keys.index(prev2_vertex_pair)

			prev2_vertex_pair = list(prev2_vertex_pair)
			prev2_vertex_pair[prev2_vertex_pair.index(seg2_vfirst)] = seg1_vfirst
			prev2_vertex_pair = tuple(prev2_vertex_pair)
			new_vertex_edge_map_keys[prev2_vertex_pair_index] = prev2_vertex_pair

			new_vertex_edge_map_keys = new_vertex_edge_map_keys[:prev2_vertex_pair_index+1] + segment1 + new_vertex_edge_map_keys[prev2_vertex_pair_index+1+length2:]
			next2_vertex_pair_index = new_vertex_edge_map_keys.index(next2_vertex_pair)
			next2_vertex_pair = list(next2_vertex_pair)
			next2_vertex_pair[next2_vertex_pair.index(seg2_vend)] = seg1_vend
			next2_vertex_pair = tuple(next2_vertex_pair)
			new_vertex_edge_map_keys[next2_vertex_pair_index] = next2_vertex_pair

			new_vertex_edge_map = list(vertex_edge_map)

			new_vertex_pairs = list_of_vertex_pairs(new_vertex_edge_map)

			del new_vertex_pairs[random_subgraph]
			new_vertex_pairs.insert(random_subgraph, new_vertex_edge_map_keys)
	
	return new_vertex_pairs

def list_of_vertex_pairs(vertex_edge_map):
	vertex_pairs_list = []
	for graph in vertex_edge_map:
		 vertex_pairs_list.append(list(graph.keys()))

	return vertex_pairs_list

def index_to_xy(graph_list, vertex):
	graph_list_xy = []
	for graph in graph_list:
		graph_xy = []
		for index in graph:
			graph_xy.append(vertex[index])
		graph_list_xy.append(graph_xy)
	return graph_list_xy

# MAIN
graph_list = []
graph_list.append(range(len(vertex)))

vertex_edge_map_initial = []
for graph in graph_list:
	temp = []
	for i in range(len(graph) -1):
		temp.append(tuple((i,i+1)))
	vertex_edge_map_initial.append(temp)

# this will have to be randon
vertex_edge_map_initial = vertex_edge_map(vertex_edge_map_initial)

features = getGraph(list_of_vertex_pairs(vertex_edge_map_initial), vertex)
# print(features)

vertex_score = all_vertex_score(features)
edge_score = all_edge_score(features)
# print(vertex_score)
# print(edge_score)

# need to change
# print(vertex_edge_map_initial)

# scatter(graph_list)
plot(vertex_edge_map_initial, vertex)
plt.show()

# m1
vertex_edge_map_m1, removed_segement, graph_list_m1 = move1(vertex_edge_map_initial, vertex_score, edge_score, graph_list)
plot(vertex_edge_map_m1, vertex)
plt.show()


# change the order of the vertex (regraph)
# vertex_m1 = regraph(vertex_edge_map_m1, vertex)

# calculate features
features_m1 = getGraph(list_of_vertex_pairs(vertex_edge_map_m1), vertex)
vertex_score_m1 = all_vertex_score(features_m1)
edge_score_m1 = all_edge_score(features_m1)

# need to change
vertex_edge_map_m1 = vertex_edge_map(list_of_vertex_pairs(vertex_edge_map_m1))

# m2
vertex_edge_map_m2, graph_list_m2 = move2(vertex_edge_map_m1, removed_segement, graph_list_m1, vertex_score_m1)
plot(vertex_edge_map_m2, vertex)
plt.show()

# this needs to be changed
features_m2 = getGraph(list_of_vertex_pairs(vertex_edge_map_m2), vertex)
vertex_score_m2 = all_vertex_score(features_m2)
edge_score_m2 = all_edge_score(features_m2)

# move3
vertex_edge_map_m3, removed_segment_m3, graph_list_m3 = move1(vertex_edge_map_m2, vertex_score_m2, edge_score_m2, graph_list_m2)

# this needs to be changed
features_m3 = getGraph(list_of_vertex_pairs(vertex_edge_map_m3), vertex)
vertex_score_m3 = all_vertex_score(features_m3)
edge_score_m3 = all_edge_score(features_m3)

# need to change
vertex_edge_map_m3 = vertex_edge_map(list_of_vertex_pairs(vertex_edge_map_m3))


vertex_edge_map_m3, graph_list_m3 = move2(vertex_edge_map_m3, removed_segment_m3, graph_list_m3, vertex_score_m3)
plot(vertex_edge_map_m3, vertex)
plt.show()

# print(vertex_edge_map_m3)
# print(graph_list_m3)

# move4
vertex_edge_map_m4, graph_list_m4 = move4(vertex_edge_map_m3, graph_list_m3, vertex_score_m3)
# print(vertex_edge_map_m4)
# print(graph_list_m4)
plot(vertex_edge_map_m4, vertex)
plt.show()

# this needs to be changed
features_m4 = getGraph(list_of_vertex_pairs(vertex_edge_map_m4), vertex)
vertex_score_m4 = all_vertex_score(features_m4)
edge_score_m4 = all_edge_score(features_m4)

# need to change
vertex_edge_map_m4 = vertex_edge_map(list_of_vertex_pairs(vertex_edge_map_m4))
# print(vertex_edge_map_m4)

vertex_pair_list_m5 = move5(vertex_edge_map_m4, graph_list_m4, vertex_score_m4, edge_score_m4)
vertex_edge_map_m5 = vertex_edge_map(vertex_pair_list_m5)
plot(vertex_edge_map_m5, vertex)
plt.show()
# sys.exit()

# this needs to be changed
# features_m5 = getGraph(index_to_xy(graph_list_m4, vertex))
# vertex_score_m5 = all_vertex_score(features_m5)
# edge_score_m5 = all_edge_score(features_m5)

# need to change
# vertex_edge_map_m5 = vertex_edge_map(graph_list_m5)
# print(vertex_edge_map_m5)
vertex_pair_list_m6 = []

while len(vertex_pair_list_m6) == 0:
	vertex_pair_list_m6 = move6(vertex_edge_map_m5)
	
vertex_edge_map_m6 = vertex_edge_map(vertex_pair_list_m6)
plot(vertex_edge_map_m6, vertex)
plt.show()
# sys.exit()
