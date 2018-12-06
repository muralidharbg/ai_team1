import collections
import numpy as np
import matplotlib.pyplot as plt

vertex = [[1,1],[2,2],[2,5],[2,7],[3,3],[3,3],[3,8],[4,2],[4,4],[4,7],[5,1],[5,5],[5,6]]
# vertex = [[1,1],[2,2],[3,3],[4,4],[5,5],[5,6],[4,7],[3,8],[2,7],[2,5],[3,3],[4,2],[5,1]]
weights = {
	"v": [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
	"e": [[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
}
features = {
	"v": [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
	"e": [[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
}

def calculate_vertex_score(i):
	value = k = 0
	for k in range(3):
		value += weights["v"][i][k] * features["v"][i][k]
	
	return value

def all_vertex_score():
	vertex_score = []
	try:
		for i in range(len(features["v"])):
			vertex_score.append(calculate_vertex_score(i))
	except Exception as e:
		print("Error calculating vertex score.", e)
	finally:
		return vertex_score

def calculate_edge_score(i):
	value = k = 0
	for k in range(4):
		value += weights["e"][i][k] * features["e"][i][k]
	
	return value

def all_edge_score():
	edge_score = []
	try:
		for i in range(len(features["e"])):
			edge_score.append(calculate_edge_score(i))

	except Exception as e:
		print("Error calculating edge score.", e)
	finally:
		return edge_score

def vertex_edge_map():
	j = 0
	vertex_edge_map = collections.OrderedDict()
	
	for i in range(len(vertex) - 1):
		vertex_edge_map[(i,i+1)] = j
		j += 1
	
	return vertex_edge_map

vertex_score = all_vertex_score()
edge_score = all_edge_score()

vertex_edge_map = vertex_edge_map()

def scatter(vertex):
	data = np.array(vertex)
	x, y = data.T

	plt.scatter(x,y)
	
def plot(vertex_edge_map):
	data = np.array(vertex)
	x, y = data.T

	plt.scatter(x,y)
	for vertex_pair, edge in vertex_edge_map.items():
		vertex1, vertex2 = vertex_pair
		x = [data[vertex1][0],data[vertex2][0]]
		y = [data[vertex1][1],data[vertex2][1]]
		plt.plot(x,y,'-o')

scatter(vertex)
plot(vertex_edge_map)
plt.show()

# m1
all_segement_score = collections.OrderedDict()

for vertex_pair, edge in vertex_edge_map.items():
	vertex1, vertex2 = vertex_pair
	segment_score = vertex_score[vertex1] + vertex_score[vertex2] + edge_score[edge]
	all_segement_score[vertex_pair] = segment_score

min_segement = min(all_segement_score, key=all_segement_score.get)

# print(min_segement)

vertex_edge_map_m1 = vertex_edge_map
del vertex_edge_map_m1[min_segement]

plot(vertex_edge_map_m1)
plt.show()

# m2

