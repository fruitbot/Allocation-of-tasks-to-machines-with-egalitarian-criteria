import random
from operator import itemgetter

def create_LM(nb_machines, max_weight):
    LM = [{"name": machine, "LTM": []} for machine in range(nb_machines)]
    return LM


def create_LT(nb_tasks, nb_types, max_weight):
    random.seed()
    LT = [{"type" : random.randint(1, nb_types) , "size" : random.randint(1, max_weight+1) } for task in range(nb_tasks)]
    return LT


def total_cost_M_1type(M):
    """Function to use when there's only one type of tasks in LM
        returns the total cost of a machine M
        It justs add all tasks' weight in the machine M
        N.B. : a machine is an array of tasks : [ [type,weight] , ... , [type,weight] ]
        """
    if isinstance(M['LTM'], list):
        return sum(t for t in M['LTM'])
    
    return sum(T['size']for T in M['LTM'])
    
    
def min_ind_cost_LM_1type(LM):
    """Function to use when there's only one type of tasks in LM
        returns the machine's index that costs the less"""
    
    #initialisation
    min_cost=total_cost_M_1type(LM[0])
    min_ind=0
    
    #search
    for i in range(0,len(LM)):
        tmp_cost = total_cost_M_1type(LM[i])
        if (tmp_cost<min_cost):
            min_cost=tmp_cost
            min_ind=i
        
    return min_ind
    
def max_ind_cost_LM_1type(LM):
    """Function to use when there's only one type of tasks in LM
        returns the machine's index that costs the most"""
    
    #initialisation
    max_cost=total_cost_M_1type(LM[0])
    max_ind=0
    
    #search
    for i in range(0,len(LM)):
        tmp_cost = total_cost_M_1type(LM[i])
        if (tmp_cost>max_cost):
            max_cost=tmp_cost
            max_ind=i
        
    return max_ind
    
def final_cost_LM_1type(LM):
    """Function to use when there's only one type of tasks in LM
        returns the maximal cost amongs all machines
            i.e. the biggest cost 
    """
    return total_cost_M_1type(LM[max_ind_cost_LM_1type(LM)])

def lpt(LM, LT, MCoeff = None, k = 0):
    """Algorithm : Largest Processing Time
        returns a list of machines containing tasks : 
        [ [[type,weight],...,[type,weight]] ,
          ... 
          , [[type,weight],...,[type,weight]] ]
        """
    LT_sorted = sorted(LT, key = itemgetter('size'))
    LM_lpt=LM
    
    for i in range(0,len(LT)):
        """
        if (i<len(LM_lpt)):
                LM_lpt[i]['LTM'].append(LT_sorted[len(LT)-1-i])
        else:
        """
        LM_lpt[min_ind_cost_LM_1type(LM_lpt)]['LTM'].append(LT_sorted[len(LT)-1-i])
        
    return LM_lpt

def lpt_1type(LM, LT):
    LT_sorted = sorted(LT)
    LM_lpt=LM
    
    for i in range(0,len(LT)):
        """
        if (i<len(LM_lpt)):
                LM_lpt[i]['LTM'].append(LT_sorted[len(LT)-1-i])
        else:
        """
        LM_lpt[min_ind_cost_LM_1type(LM_lpt)]['LTM'].append(LT_sorted[len(LT)-1-i])
        
    return LM_lpt
        
def lpt_mixed(LM, LT1, LT2) :
    # merge LT1 and LT2
    LT = LT1 + LT2
    return lpt(LM, LT)

def affichage_lm(LM,nb_machines):
    tmp=""
    for i in range(0,nb_machines):
        for j in range(0,len(LM[i]['LTM'])):
            tmp+="\t"+str(LM[i]['LTM'][j]['size'])
        print(tmp)
        tmp=""
        print("")
    return