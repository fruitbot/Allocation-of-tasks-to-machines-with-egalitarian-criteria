"for algorithms involved in the calculation of costs"

def cost_M_gen(M,MCoeff):
    """input : machine M * matrix types' coefficient
        output : the cost of the machine
        Function use in greedy_cluster verifying if the machine's cost is > esp*LB
    """
    # C is a list containing all tasks' cost in the machine
    C=[]
    # for each task, we calculate its cost and add it in C
    for t in M['LTM']:
        tmp=0
        for t2 in M['LTM']:
            tmp+=float(MCoeff[t['type']-1][t2['type']-1])*t2['size']
        C.append(tmp)
    #if C is not empty i.e. M is not empty, trying max(C) when C is empty results as an error
    if len(C):
        return max(C)
    else:
        return 0
    
def cost_final_LM_gen(LM,MCoeff):
    """input : list of machines * matrix types' coefficient
        output : (list of machines)'s cost
        Alternative of Shuting's version using cost_M_gen
    """
    C=[]
    for M in LM:
        C.append(cost_M_gen(M,MCoeff))
    return max(C)

    
def min_ind_cost_LM_gen(LM,MCoeff):
    """input : list of machines * matrix types' coefficient
        output : machine's index having the minimal cost
    """
    C=[]    
    for M in LM:
        C.append(cost_M_gen(M,MCoeff))
    return C.index(min(C))

    
def max_ind_cost_LM_gen(LM,MCoeff):
    """input : list of machines * matrix types' coefficient
        output : list of machine's index having the maximal cost
    """
    most_charged_machines = []
    cost_max = 0

    for M in range(len(LM)):
        new_cost = cost_M_gen(LM[M],MCoeff)
        if new_cost >= cost_max:
            most_charged_machines.append(M)
            cost_max = new_cost

    return most_charged_machines
