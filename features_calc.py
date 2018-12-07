import math
import json

angles = list()

def dot(x1, y1, x2, y2):
    return x1*x2 + y1*y2

def norm(x,y):
    return math.sqrt(math.pow(x,2) + math.pow(y,2))

def lenEdge(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))

def angle(x1, y1, x2, y2):
    angles.append(math.cos(math.degrees(math.acos(dot(x1, y1, x2, y2)/(norm(x1, y1)*norm(x2,y2))))))
    return math.cos(math.degrees(math.acos(dot(x1, y1, x2, y2)/(norm(x1, y1)*norm(x2,y2)))))

def diffAngles(angle1, angle2):
    return angle2 - angle1

def calcFeatures(graph):
    global angles
    for i in range(len(graph)):
        if len(graph) is 1:
            V = [0,0,0]
        elif i+1 < len(graph):
            V = [1,angle(graph[i][0], graph[i][1], graph[i+1][0], graph[i+1][1]), math.pow(angle(graph[i][0], graph[i][1], graph[i+1][0], graph[i+1][1]),2)]
        else:
            V = [1,0,0]

        if i>0 and i+1 < len(graph):
            E = [lenEdge(graph[i][0], graph[i][1], graph[i+1][0], graph[i+1][1]), math.pow(lenEdge(graph[i][0], graph[i][1], graph[i+1][0], graph[i+1][1]),2), diffAngles(angles[i-1], angles[i]), math.pow(diffAngles(angles[i-1], angles[i]),2)]
        elif i+1 < len(graph):
            E = [lenEdge(graph[i][0], graph[i][1], graph[i+1][0], graph[i+1][1]), math.pow(lenEdge(graph[i][0], graph[i][1], graph[i+1][0], graph[i+1][1]),2), 0, 0]
        else:
            E = [0, 0, diffAngles(angles[i-1], angles[i]), math.pow(diffAngles(angles[i-1], angles[i]),2)]

        features['V'].append(V)
        features['E'].append(E)


def getGraph(graphList):
    for graph in graphList:
        features = calcFeatures(graph)
