""" --- data structure --- """
#machines : list of several 'machine'
#machine : dictionary : has a "name" and a "LT" (tasks)
#tasks : list of several 'task'
#task : basic dictionary

""" ___ conventions ____ """
# LT __ List of Tasks __
# T  __ Task ___
# LM __ List of machines __
# M  __ Machine __
# LTM __ List of Tasks in the Machine __
# LW __ List of Weights __
# MCoeff __ matrix of coefficients of compatibility between tasks __

import random
import numpy as np
import copy
import math

def borne_inf(LT, LM):
    #max_task = max(LT[]['size'])
    max_task = max(task['size'] for task in LT)
    av = sum(task['size'] for task in LT)/len(LM)
    #print(np.max(MCoeff))
    return max(max_task, av)

def borne_inf_1type(LT, LM):
    print(LT)
    max_task = np.max(LT)
    av = sum(LT)/len(LM)
    #print(np.max(MCoeff))
    return max(max_task, av)

def inf_sup(LT, LM):
    LB = borne_inf(LT, LM)
    return LB, 2*LB

def inf_sup_1type(LT, LM):
    LB = borne_inf_1type(LT, LM)
    return LB, 2*LB

def LB_types(LT, LM, MCoeff):
    LT_type = [[t["size"] for t in LT if t["type"] == typ] for typ in range(len(MCoeff))]
    av_type = [sum(LT_1type)/len(LT_1type) for LT_1type in LT_type if len(LT_1type) != 0 ]
    max_task = max(task['size'] for task in LT)
    print(max(av_type), max_task)
    return max(max(av_type), max_task)

def inf_sup_types(LT, LM, MCoeff):

    inf = LB_types(LT,LM,MCoeff)

    LB = borne_inf(LT, LM)
    sup = 2 * LB * np.max(MCoeff)
    print(inf, sup)
    return inf, sup


def print_lm(LM,nb_machines):
    """
    Only use for debugs and WIP functions, please use tkinter when done
    print in a simple yet useful way LM
    """
    tmp=""
    for i in range(0,nb_machines):
        for j in range(0,len(LM[i]['LTM'])):
            tmp+="\t"+str(LM[i]['LTM'][j]['type'])+","+str(LM[i]['LTM'][j]['size'])
        print("machine ",i+1,"\t",tmp)
        tmp=""
        print("")
    return


def create_A_alpha(n,max_alpha):
    """creates a random matrix containing the compatibility coefficient between each types
                n : the size
        max_alpha : maximum coefficient (excluded) 
    """
    #random matrix values : [0 to 1[
    A=np.random.rand(n,n)
    
    #
    for i in range(n):
        for j in range(n):
            A[i][j]*=max_alpha
            
    A=np.tril(A,-1) #transforms A to a matrix triangular lower with the diagonal filled with 0
    B=A.T #B is now the transposition of A, but A did not change
    C=A+B 
    np.fill_diagonal(C,1) # C's diagonal is now filled with 1
    return C

def M_Coeff_intervalle(n, a, b):

    """creates a random matrix containing the compatibility coefficient between each types
                n : the size
        max_alpha : maximum coefficient (excluded) 
    """
    #random matrix values : [0 to 1[
    A=np.random.rand(n,n)*(b - a) + a
            
    B = (A + A.T ) / 2

    np.fill_diagonal(B,1) # C's diagonal is now filled with 1
    
    return B


def M_Coeff_intervals(n, intervals, probas):

    values = []

    for i in range(len(probas)):
        values.append(np.random.random(math.ceil(probas[i] * n * (n - 1) / 2)) * (intervals[i][1] - intervals[i][0]) + intervals[i][0])

    values = np.array(values).flatten()
    # shuffle values
    np.random.shuffle(values)

    # fill upper triangular matrix
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(i): # diagonal excluded
            A[i, j] = values[(i-1)*(i)//2 + j] # // to cast into int, but no decimal anyway

    A = (A + A.T)
    
    np.fill_diagonal(A, 1)

    return A


def create_LM(nb_machines):
    LM = [{"name": machine + 1, "LTM": []} for machine in range(nb_machines)]
    return LM


def create_LT(nb_tasks, nb_types, max_weight):
    random.seed()
    LT = [{"type" : random.randint(1, nb_types ) , "size" : random.randint(1, max_weight+1) } for task in range(nb_tasks)]
    return LT
    
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
        if new_cost == cost_max:
            most_charged_machines.append(M)
        if new_cost > cost_max:
            most_charged_machines = [M]
            cost_max = new_cost

    return most_charged_machines


def affichage_lm(LM,nb_machines):
    tmp=""
    if nb_machines == 1:
        print("")
    else:
        for i in range(0,nb_machines):
            for j in range(0,len(LM[i]['LTM'])):
                tmp+="\t"+str(LM[i]['LTM'][j]['type'])+','+str(LM[i]['LTM'][j]['size'])
            print(tmp)
            tmp=""
            print("")
    return

def cost_max(LM, LT, Mcoeff):
    list_of_sum_of_machine = []
    list_of_sum_of_LM = []
    for i in range(0, len(LM)): #for every machine in LM
        for j in range(0, len(LM[i]['LTM'])): #for every task in one machine
            target_task_type = LM[i]['LTM'][j]['type']#get the type of the target task in the machine, from 1st task to the last
            sum = LM[i]['LTM'][j]['size'] #initialise with the cost of the target task in the machine
            for l in range(0, len(LM[i]['LTM'])): #this loop is to calculate the sum with corresponding coeff
                if LM[i]['LTM'][j] != LM[i]['LTM'][l]:

                    sum += LM[i]['LTM'][l]['size'] * (Mcoeff[target_task_type-1][(LM[i]['LTM'][l]['type'])-1]).astype(float)
                
                list_of_sum_of_machine.append(sum)
            max_of_machine = max(list_of_sum_of_machine) #max cost for current machine
            list_of_sum_of_LM.append(max_of_machine) #put⬆them in this list
        #print("list:", list_of_sum_of_LM, "\n")
        if list_of_sum_of_LM:
            max_of_LM = max(list_of_sum_of_LM) #max cost for the whole LM
    return max_of_LM #Ta-da

#end

def OrderTypeCostMax(nbLM, LT, Mcoeff):
    LM = create_LM(nbLM)
    LMO = order_type_final(LM, LT, Mcoeff)
    return cost_max(LMO, Mcoeff)


def verif_tasks(LM, LT):
    LT_temp = []
    for i in range(0, len(LM)):
        for task in LM[i]['LTM']:
            LT_temp.append(task)

    if (len(LT_temp) > len(LT)):
        print("Duplicating tasks : ", len(LT_temp) - len(LT))
        return
    if (len(LT_temp) < len(LT)):
        print("Missing tasks : ", len(LT) - len(LT_temp))
        return
    if (not (all(elem in LT_temp for elem in LT) and all(elem in LT for elem in LT_temp))):
        print("Duplicating n tasks and missing n tasks")

    if (len(LT_temp)>len(LT)):
        print("Duplicating tasks : ",len(LT_temp)-len(LT))
        return
    if (len(LT_temp)<len(LT)):
        print("Missing tasks : ",len(LT)-len(LT_temp))
        return
    if (not (all(elem in LT_temp for elem in LT) and all(elem in LT for elem in LT_temp))):
        print("Duplicating n tasks and missing n tasks")
        return
    print("All is good")
    return


def LM_group_by_type(LM):
    LM_grouped = create_LM(len (LM))
    for k in range (len (LM)):
        LM_grouped[k] = copy.deepcopy (M_group_by_type (LM [k]))
    return LM_grouped


def M_group_by_type(M):
    S_type=[]
    for task in M['LTM']:
        if (task['type']<=len(S_type)):
            S_type[task['type']-1]+=task['size']
        else:
            while(task['type']>len(S_type)):
                S_type.append(0)
            S_type[task['type']-1]+=task['size']

    if (len (S_type)==0):
        return M
    M_grouped = {"name": M['name'], "LTM": []}
    for k in range(len (S_type)):
        M_grouped['LTM'].append({"type": k+1, "size": S_type[k]})
    for task in M_grouped['LTM']:
        if task['size']==0:
            M_grouped['LTM'].remove(task)
    return M_grouped


########################## LIST OF ALGORITHMS ###########################
# * lpt 
#
# * schJuxtaposed
#
# * greedy_cluster_improved
#
# * mixed
#
# * order_type
#
# * order_type_greedy

