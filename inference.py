import collections
from features import phi1, phi2, phi4, vertex_edge_map, edge_weights

def find_connected_edges(i):
	edge1 = edge2 = None
	found = False
	edge1_list = []
	edge2_list = []
	phi4_value = None
	vertex_edge_map_keys = vertex_edge_map.keys()
	# while(not found):
	for vertex_pair1 in vertex_edge_map_keys:
		if vertex_pair1[-1] == i and vertex_pair1 not in edge1_list:
			edge1 = vertex_edge_map[vertex_pair1]
			edge1_list.append(vertex_pair1)
			# break
			print("edge1: ", edge1)
			for vertex_pair2 in vertex_edge_map_keys:
				if vertex_pair2[0] == i and vertex_pair2 not in edge2_list:
					edge2 = vertex_edge_map[vertex_pair2]
					print("edge2: ", edge2)
					edge2_list.append(vertex_pair2)
					# break
					if (edge1,edge2) in phi4.keys():
						found = True
						break

		if found == True:
			print("asdasd")
			break
		else:
			edge2_list = []

	return [edge1,edge2]


def calculate_vertex_score(i):
	value = k = edge1 = edge2 = 0
	value += vertex_weights[i][k] * phi1[i]
	k += 1
	print("qqqq")
	if i == 0 or i == len(phi1) - 1:
		value += vertex_weights[i][k] * 1
	else:
		# find egde (?,i) and (i,?)
		edge1,edge2 = find_connected_edges(i)
		if (edge1,edge2) in phi4:
			phi4_value = phi4[(edge1,edge2)]
		else:
			raise Exception("Could not find edges associated with vertex " + i)

		value += vertex_weights[i][k] * phi4_value
	
	k += 1

	if i == 0 or i == len(phi1) - 1:
		value += vertex_weights[i][k] * 1
	else:
		value += vertex_weights[i][k] * phi5[edge1,edge2]

	return value

def find_next_edge(vertex_pair):
	vertex_edge_map_keys = vertex_edge_map.keys()
	i,j = vertex_pair
	found = False
	
	edge1 = vertex_edge_map[vertex_pair]
	edge2_list = []

	for vertex_pair2 in vertex_edge_map_keys:
		if vertex_pair2[0] == j and vertex_pair2 not in edge2_list:
				edge2 = vertex_edge_map[vertex_pair2]
				edge2_list.append(vertex_pair2)
				if (edge1,edge2) in phi4.keys():
					found = True
					break

	if found == True:
		return vertex_pair2
	else:
		return None

def find_prev_edge(vertex_pair):
	vertex_edge_map_keys = vertex_edge_map.keys()
	i,j = vertex_pair
	found = False
	
	edge1 = vertex_edge_map[vertex_pair]
	edge2_list = []

	for vertex_pair2 in vertex_edge_map_keys:
		if vertex_pair2[-1] == i and vertex_pair2 not in edge2_list:
			edge2 = vertex_edge_map[vertex_pair2]
			edge2_list.append(vertex_pair2)
			if (edge2,edge1) in phi4.keys():
				found = True
				break

	if found == True:
		return vertex_pair2
	else:
		return None

def find_consecutive_angle(edge1,edge2):
	consecutive_angle = None
	for key in phi4.keys():
		if key[0] == edge2:
			consecutive_angle = key
			break

	return consecutive_angle

def calculate_edge_score(vertex_pair):
	value = k = 0
	
	current_edge_weights = edge_weights[vertex_edge_map[vertex_pair]]

	value += current_edge_weights[k] * phi2[vertex_edge_map[vertex_pair]]
	
	k += 1
	value += current_edge_weights[k] * phi3[vertex_edge_map[vertex_pair]]
	
	k += 1
	
	if vertex_pair == (0,1):
		vertex_pair2 = find_next_edge(vertex_pair)
		# cosine of 360 degree = 1
		angle_diff = 1 - phi4[vertex_edge_map[vertex_pair],vertex_edge_map[vertex_pair2]]
		value += current_edge_weights[k] * angle_diff

		k += 1
		value += current_edge_weights[k] * (angle_diff ** 2)
	elif vertex_pair == (14,15):
		vertex_pair2 = find_prev_edge(vertex_pair)
		# cosine of 360 degree = 1
		angle_diff = phi4[vertex_edge_map[vertex_pair2],vertex_edge_map[vertex_pair]] - 1
		value += current_edge_weights[k] * angle_diff

		k += 1
		value += current_edge_weights[k] * (angle_diff ** 2)
	else:
		vertex_pair2 = find_next_edge(vertex_pair)
		edge1 = vertex_edge_map[vertex_pair]
		edge2 = vertex_edge_map[vertex_pair2]
		adjacent_edge_pair = find_consecutive_angle(edge1,edge2)

		if adjacent_edge_pair == None:
			vertex_pair2 = find_prev_edge(vertex_pair)
			edge2 = vertex_edge_map[vertex_pair2]
			adjacent_edge_pair = find_consecutive_angle(edge2,edge1)
		
			if adjacent_edge_pair == None:
				raise Exception("adjacent_edge_pair could not be found for vertex_pair: " + vertex_pair)

			angle_diff = phi6[((edge2,edge1),(adjacent_edge_pair))]
			angle_diff_sq = phi7[((edge2,edge1),(adjacent_edge_pair))]
		else:
			angle_diff = phi6[((edge1,edge2),(adjacent_edge_pair))]
			angle_diff_sq = phi7[((edge1,edge2),(adjacent_edge_pair))]
		
		value += current_edge_weights[k] * angle_diff

		k += 1
		value += current_edge_weights[k] * angle_diff_sq

	return value

def all_vertex_score():
	vertex_score = []
	try:
		for i in range(len(phi1)):
			vertex_score.append(calculate_vertex_score(i))
	except Exception as e:
		print("Error calculating vertex score.", e)
	finally:
		return vertex_score

def all_edge_score():
	edge_score = collections.OrderedDict()
	try:
		for i in vertex_edge_map.keys():
			edge_score[vertex_edge_map[i]] = calculate_edge_score(i)

	except Exception as e:
		print("Error calculating edge score.", e)
	finally:
		return edge_score


def get_rope_configuration():
	return {"phi1": phi1, "phi2": phi2, "phi3": phi3, "phi4": phi4, "phi5": phi5, "phi6": phi6, "phi7": phi7, "phi8": phi8, "vertex_score": vertex_score, "edge_score": edge_score}

def total_graph_score():
	return sum(vertex_score) + sum(edge_score.values())

def calculate_phi3():
	phi3 = collections.OrderedDict()

	for edge,length in phi2.items():
		phi3[edge] = length ** 2

	return phi3

def calculate_phi5():
	phi5 = collections.OrderedDict()
	for edges,angle_cosine in phi4.items():
		phi5[edges] = angle_cosine ** 2

	return phi5

def calculate_phi6():
	phi6 = collections.OrderedDict()
	phi4_keys = list(phi4.keys())

	for i in phi4.keys():
		edge_pair1 = i
		adjacent_edge_pair = find_consecutive_angle(edge_pair1[0],edge_pair1[1])
		if adjacent_edge_pair != None:
			diff = phi4[edge_pair1] - phi4[adjacent_edge_pair]
			phi6[(edge_pair1,adjacent_edge_pair)] = diff

	return phi6

def calculate_phi7():
	phi7 = collections.OrderedDict()
	for i in phi6.keys():
		phi7[i] = phi6[i] ** 2

	return phi7

phi3 = calculate_phi3()
phi5 = calculate_phi5()
phi6 = calculate_phi6()
phi7 = calculate_phi7()

phi8 = 9

vertex_weights = [[1, 2, 3],[1, 2, 3],[1, 2, 3],[1, 2, 3],[1, 2, 3],[1, 2, 3],[1, 2, 3],[1, 2, 3],[1, 2, 3],[1, 2, 3],[1, 2, 3],[1, 2, 3],[1, 2, 3],[1, 2, 3],[1, 2, 3]]

vertex_score = all_vertex_score()
edge_score = all_edge_score()

r_prime_initial = get_rope_configuration()
r_prime_initial["graph_score"] = total_graph_score()

print("initial")
print("graph_score: ", r_prime_initial["graph_score"])

# m1
print("m1")
min_vertex_score = []
while True:
	min_score = None
	for score in vertex_score:
		if min_score == None or (score < min_score and vertex_score.index(score) not in min_vertex_score):
			min_score = score

	least_scoring_segment = vertex_score.index(min_score)
	if(phi1[least_scoring_segment] == 1):
		print("least_scoring_segment: ", least_scoring_segment)
		phi1[least_scoring_segment] = 0
		break
	else:
		min_vertex_score.append(least_scoring_segment)

vertex_score = all_vertex_score()
edge_score = all_edge_score()

r_prime_m1 = get_rope_configuration()
r_prime_m1["graph_score"] = total_graph_score()
print("graph_score: ", r_prime_m1["graph_score"])

# m2
print("m2")
excluded_segment = phi1.index(min(phi1))
print("excluded_segment: ", excluded_segment)
phi1[excluded_segment] = 1

vertex_score = all_vertex_score()
edge_score = all_edge_score()

r_prime_m2 = get_rope_configuration()
r_prime_m2["graph_score"] = total_graph_score()
print("graph_score: ", r_prime_m2["graph_score"])

# m3
print("m3")
first_segment = phi1.pop(0)
phi1.append(first_segment)

vertex_edge_map_values = list(vertex_edge_map.values())

first_segment = vertex_edge_map_values.pop(0)
vertex_edge_map_values.append(first_segment)

i = 0
for key in vertex_edge_map.keys():
	vertex_edge_map[key] = vertex_edge_map_values[i]
	i += 1


# phi2 needs to be recalculated

phi2_values = list(phi2.values())

first_segment = phi2_values.pop(0)
phi2_values.append(first_segment)

i = 0
for key in phi2.keys():
	phi2[key] = phi2_values[i]
	i += 1


phi3 = calculate_phi3()

# phi4 needs to be recalculated
phi4_values = list(phi4.values())

first_segment = phi4_values.pop(0)
phi4_values.append(first_segment)

i = 0
for key in phi4.keys():
	phi4[key] = phi4_values[i]
	i += 1


phi5 = calculate_phi5()

phi6 = calculate_phi6()

phi7 = calculate_phi7()


vertex_score = all_vertex_score()
edge_score = all_edge_score()

r_prime_m3 = get_rope_configuration()
r_prime_m3["graph_score"] = total_graph_score()
