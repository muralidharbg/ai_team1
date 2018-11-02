def vertex_sum(vertexs):
    value = 0
    for vertex in vertexs:
        weights = vertex["weights"]
        features = vertex["features"]
        for i in range(0, len(weights)):
            value += weights[i] * features[i]

    return value


def edge_sum(edges):
    value = 0
    for edge in edges:
        weights = edge["weights"]
        features = edge["features"]
        for i in range(0, len(weights)):
            value += weights[i] * features[i]

    return value

def score(graph):
    return (1/len(graph["V"]))*vertex_sum(graph["V"]) + (1/len(graph["E"]))*edge_sum(graph["E"])

vertex1 = {"weights": [1, 2, 3], "features": [1, .70711, .5]}
vertex2 = {"weights": [1, 2, 3], "features": [1, .86603, .75]}
vertex3 = {"weights": [1, 2, 3], "features": [1, .64279, .41318]}

edge1 = {"weights": [1, 2, 3, 4], "features": [3, 9, -.15892, -.02526]}
edge2 = {"weights": [1, 2, 3, 4], "features": [4, 16, .22324, .04984]}

graph = {"V": [vertex1, vertex2, vertex3], "E": [edge1, edge2]}

print(score(graph))
