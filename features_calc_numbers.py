import math
import json

def lenEdge(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))

def angle(p1, p2, p3):
    power = (math.pow(lenEdge(p1[0],p1[1],p2[0],p2[1]),2) + math.pow(lenEdge(p1[0],p1[1],p3[0],p3[1]),2) - math.pow(lenEdge(p2[0],p2[1],p3[0],p3[1]),2)) / (2*lenEdge(p1[0],p1[1],p2[0],p2[1])*lenEdge(p1[0],p1[1],p3[0],p3[1]))
    if power < -1:
        power = -1
    
    if power > 1:
        power = 1

    acos = math.acos((power))
    return math.cos(math.degrees(acos))

def diffAngles(angle1, angle2):
    return angle2 - angle1

def calcFeatures(graph):
    features = {'V': list(), 'E': list()}
    angles = list()
    vertices = list()
    for i in range(len(graph)):
        vertex1 = graph[i][0]
        vertex2 = graph[i][1]
        if len(vertices) is 0:
            angles.append(0)
            features['V'].append([1,0,0])

            added = False
            for j in range(i+1, len(graph)): 
                if graph[j][0][0] == vertex2[0] and graph[j][0][1] == vertex2[1]:
                    angles.append(angle(vertex2,vertex1,graph[j][1]))
                    V2 = [1,angle(vertex2,vertex1,graph[j][1]), math.pow(angle(vertex2,vertex1,graph[j][1]),2)]
                    features['V'].append(V2)
                    added = True
                    break
                
                
            if added == False:
                V2 = [1,0,0]
                angles.append(0)
                features['V'].append(V2)

            vertices.append(vertex1)
            vertices.append(vertex2)
        else:
            found = False

            for vertex in vertices:
                # if vertex2 == [4,4]:
                #     print(f'vertex: {vertex}')
                #     print(f'vertex2: {vertex2}')
                if vertex[0] == vertex2[0] and vertex[1] == vertex2[1]:
                    found = True
                    # print("hi")
                    break
            
            if found == False:
                added = False
                for j in range(i+1, len(graph)): 
                    if graph[j][0][0] == vertex2[0] and graph[j][0][1] == vertex2[1]:
                        angles.append(angle(vertex2,vertex1,graph[j][1]))
                        V2 = [1,angle(vertex2,vertex1,graph[j][1]), math.pow(angle(vertex2,vertex1,graph[j][1]),2)]
                        features['V'].append(V2)
                        added = True
                        break
                
                
                if added == False:
                    V2 = [1,0,0]
                    angles.append(0)
                    features['V'].append(V2)

                vertices.append(vertex1)
                vertices.append(vertex2)

        edge = graph[i]
        if i is not 0:
            E = [lenEdge(edge[0][0], edge[0][1], edge[1][0], edge[1][1]), math.pow(lenEdge(edge[0][0], edge[0][1], edge[1][0], edge[1][1]),2), diffAngles(angles[i-1],angles[i]), math.pow(diffAngles(angles[i-1],angles[i]),2)]
        else:
            E = [lenEdge(edge[0][0], edge[0][1], edge[1][0], edge[1][1]), math.pow(lenEdge(edge[0][0], edge[0][1], edge[1][0], edge[1][1]),2),0,0]

        features['E'].append(E)

    return features


def getGraph(graphList, masterGraph):
    featureList = list()
    for graph in graphList:
        pointGraph = list()
        if len(graph) is 1:
            featureList.append({'V': [0,0,0],'E': [0,0,0,0]})

        for edge in graph:
            edgePoints = list()
            edgePoints.append(masterGraph[edge[0]])
            edgePoints.append(masterGraph[edge[1]])
            pointGraph.append(edgePoints)

        featureList.append(calcFeatures(pointGraph))

    return featureList

# graphList = [[(0,1),(1,2),(2,3),(3,4),(4,9),(4,5),(5,6),(6,7),(7,8)]]
# masterGraph = [[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9]]

# print(getGraph(graphList, masterGraph))
