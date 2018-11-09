"""
The functions related to the loss function of the learning phase

"""

def find_x_diff(correct_order, arb_label):
    min_len = min(len(correct_order), len(arb_label))
    x_list = []
    if min_len == 0:
        return x_list
    if (correct_order[0] == arb_label[0] and 
        correct_order[1] != arb_label[1]):
        x_list.append(correct_order[0])
    
    for i in range(1, min_len-1):
        if (correct_order[i] == arb_label[i] and
            correct_order[i-1] != arb_label[i-1] and
            correct_order[i+1] != arb_label[i+1] ):
            x_list.append(correct_order[i])
            
    if (correct_order[min_len] == arb_label[min_len] and 
        correct_order[min_len-1] != arb_label[min_len-1]):
        x_list.append(correct_order[min_len])
    return x_list

def find_v_val(correct_order, arb_label):
    v_list = []
    for i in range(len(correct_order)-1):
        correct_loc = -1
        count = 0
        v_sub = []
        #Not complete yet
        for j in range(len(arb_label)):
            if (arb_label[j] == correct_order[correct_loc + count] and count > 0):
                v_sub.append(arb_label[j])
            if (arb_label[j] == correct_order[i] and correct_loc == -1):
                correct_loc = i
                v_sub.append(arb_label[j])
                count = count + 1
            
                
    return v_list

def find_w_val(correct_order, arb_label):
    w_list = []
    
    return w_list



def cal_sim(correct_order, arb_label):
    x_diff = find_x_diff(correct_order, arb_label)
    V_val = find_v_val(correct_order, arb_label)
    W_val = find_w_val(correct_order, arb_label)
    
    diff_val = (x_diff + V_val^1.5 + W_val^1.5)^(1/1.5)
    return diff_val


def cal_loss(correct_order, arb_label):
    ver_count = len(correct_order)
    similarity_val = cal_sim(correct_order, arb_label)
    loss_val = (ver_count - similarity_val)/ver_count
    return loss_val
    