def vertex_sum(features, weights):
    value = 0
    for i in range(len(features['V'])):
        value += weights['V'][i] * features['V'][i]

    return value


def edge_sum(features, weights):
    value = 0
    for i in range(0, len(features['E'])):
        value += weights['E'][i] * features['E'][i]

    return value

def score(features, weights):
    return (1/len(features["V"]))*vertex_sum(features, weights) + (1/len(features["E"]))*edge_sum(features, weights)

features = {"V": [[1,2,3],[1,2,3]], "E":[1,2,3,4]}
weights = {"V":[[1,1,1],[1,1,1]],"E":[[1,1,1,1]]}

print(score(features, weights))
