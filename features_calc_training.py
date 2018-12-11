import math

def norm(x,y):
    return math.sqrt(math.pow(x,2) + math.pow(y,2))

def lenEdge(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))



def angle_calcualtor(p0, p1, p2):
    p10 = []
    p10.append(p1[0] - p0[0])
    p10.append(p1[1] - p0[1])
    p12 = []
    p12.append(p1[0] - p2[0])
    p12.append(p1[1] - p2[1])
    dot_product = p10[0]*p12[0] + p10[1]*p12[1]
    norm10 = math.sqrt(p10[0]*p10[0] + p10[1]*p10[1])
    norm12 = math.sqrt(p12[0]*p12[0] + p12[1]*p12[1])
    cos_value = dot_product / (norm10 * norm12)
    return cos_value

def diffAngles(angle1, angle2):
    return angle2 - angle1

def calcFeatures(graph):
    angles = []
    V_features = []
    E_features = []    
    for i in range(len(graph)):
        if i == 0 or i == len(graph)-1:
            V = [1,0,0]
        else:
            temp_angle = angle_calcualtor(graph[i-1], graph[i], graph[i+1])
            angles.append(temp_angle)
            V = [1,temp_angle, math.pow(temp_angle,2)]
        V_features.append(V)
    
    for i in range(len(graph)-1):

        if i> 0 and i < len(graph)-2:
            temp_len_edge = lenEdge(graph[i][0], graph[i][1], graph[i+1][0], graph[i+1][1])
            temp_diff_angles = diffAngles(angles[i-1], angles[i])
            E = [temp_len_edge, math.pow(temp_len_edge,2), temp_diff_angles, math.pow(temp_diff_angles,2)]
        elif i+1 < len(graph):
            E = [lenEdge(graph[i][0], graph[i][1], graph[i+1][0], graph[i+1][1]), math.pow(lenEdge(graph[i][0], graph[i][1], graph[i+1][0], graph[i+1][1]),2), 0, 0]
        else:
            print(i)
            E = [0, 0, diffAngles(angles[i-1], angles[i]), math.pow(diffAngles(angles[i-1], angles[i]),2)]

        
        E_features.append(E)
    return V_features, E_features
