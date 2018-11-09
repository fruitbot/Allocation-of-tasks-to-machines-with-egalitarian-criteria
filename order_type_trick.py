import sys
sys.path.append('tkinter')
import numpy as np
import data_structure
import copy
import math
import data_structure
from operator import itemgetter
import itertools



# returns borne_inf LB for makespan
# makespan is such that LB <= makespan <= 2LB
def borne_inf(LT, LM, MCoeff):
    #max_task = max(LT[]['size'])
    max_task = max(task['size'] for task in LT)
    av = sum(task['size'] for task in LT)/len(LM)
    return max(max_task, av) 

def min_sum(list_types, MCoeff):
    foo = 0
    for num_type in range(len(list_types)-1):
        foo += (float)(MCoeff[list_types[num_type]-1][list_types[num_type+1]-1])
    return foo

def min_prod(list_types, MCoeff):
    foo = 1
    for num_type in range(len(list_types)-1):
        foo *= (float)(MCoeff[list_types[num_type]-1][list_types[num_type+1]-1])
    return foo

def  order(All_types, MCoeff):

    ordered_types = []
    # or recursive function to generate perms and find min at the same time
    generator = itertools.permutations(All_types)
    min_fn = float('Inf')

    for perm in generator:
        if min_prod(perm, MCoeff) < min_fn:
            min_fn = min_prod(perm, MCoeff)
            ordered_types = perm

    #print(perm)
    #print(ordered_types)
    return ordered_types


def order_type(LM, LT, MCoeff,esp):
    """ input : List of machines, List of tasks, Array of coefficients, Double for the coefficient*LB wanted
        output : List of mahines
        order type depending on Mcoeff
        then allocate tasks with the LB criteria
        very good if not all types are compatible: because all coeffs on a machine will be 1 while they could be less if mixed
    """

    LM = data_structure.create_LM(len(LM))
    LB = borne_inf(LT, LM, MCoeff)
    #LT = sorted(LT, key = itemgetter('size'), reverse=True)

    # allocate task in the right order
    machine = 0
    for Type in ordered_types:
        for task in LT:
            # append tasks of this one type
            if task['type'] == Type:
                LM[machine]['LTM'].append(task)
                if ((data_structure.cost_M_gen(LM[machine], MCoeff)) > esp*LB ):
                   
                    LM[machine]['LTM'].remove(task)
                    # trier les taches de la machine par ordre décroissant
                    LM[machine]['LTM'] = sorted(LM[machine]['LTM'] , key = itemgetter('size'), reverse=True)
                    machine += 1

                    if (machine == len(LM)):

                        #print ("pas de machine libre")

                        return 0

                    LM[machine]['LTM'].append(task)


    # cas ou il reste des machines libres
    for machine in range(len(LM)):

        if not LM[machine]["LTM"]: # this machine is empty 

            # try to fit tasks from the most charged machine(s) on the empty machine
            most_charged = data_structure.max_ind_cost_LM_gen(LM, MCoeff)
            #print(len(most_charged))
            
            coutMax = data_structure.cost_M_gen(LM[most_charged[0]], MCoeff)

            for heavy_machine in most_charged:
                
                last_task = LM[heavy_machine]['LTM'][-1]
                # add last task to empty machine
                LM[machine]['LTM'].append(last_task)
                if data_structure.cost_M_gen(LM[machine], MCoeff) >= coutMax:
                    LM[machine]['LTM'].remove(last_task)
                    break
                # remove last task from heavy machine
                LM[heavy_machine]['LTM'].remove(last_task)
    
    return LM

def order_type_best_eps(LM,LT,MCoeff,eps_precision):
    """input : list of machines * list of tasks * matrix types'coefficient * precision of eps i.e. 1.1 ? or 1.01 ? etc (by default : 0.1)
        output : the best eps that respect the following condition - all machine's cost must be < eps*LB
       
        This function uses dichotomy to find the best eps
    """
    #print ("looking for best eps")

    #variables needed to dichotomize
    end_eps = float(4.0)
    start_eps=float(0.0)
    
    # until eps' precision is not the one wanted
    while((math.fabs(end_eps - start_eps) > eps_precision)):
        # storing the (list of machines)'s cost when eps is the midpoint of start_eps and end_eps
        #print ("start: " + str(start_eps) + " end: " + str(end_eps))
        LM_new = order_type(copy.deepcopy(LM),LT,MCoeff, (float(math.fabs(end_eps+start_eps)))/2.0)
        # the cost is not better than the actual one, i.e. eps cannot be below the midpoint
        if (LM_new == 0):
            # therefore we set the midpoint as the new start_eps
            #print ("on recupere l'ancien LB")
            start_eps = (float(math.fabs(end_eps+start_eps)))/2.0
            
        # the cost is better, i.e. eps can be below the midpoint
        else:
            A=data_structure.cost_final_LM_gen(LM_new,MCoeff)
            end_eps =(float(math.fabs(end_eps+start_eps)))/2.0
    
    return end_eps



def order_type_final(LM,LT,MCoeff, k=0):
    """input : list of machines * list of tasks * matrix types'coefficient * precision of eps i.e. 1.1 ? or 1.01 ? etc (by default : 0.0001)
        output : a new list of machines
       
        Returns the best arrangement for a list of tasks in a list of machines by using greed_clust algorithm
    """
    # create list of types
    All_types=[]
    for task in LT:
        if (task['type'] not in All_types):
            All_types.append(task['type'])

    # order types
    global ordered_types # glabal because connot be added as argument. And we dont want order() to be called all the time!
    ordered_types = order(All_types, copy.deepcopy(MCoeff))

    eps_precision=0.01
    MCoeff_copy = copy.deepcopy(MCoeff)
    LM_copy = copy.deepcopy(LM)
    eps = order_type_best_eps(LM_copy,copy.deepcopy(LT),MCoeff_copy,eps_precision)
    #print ("best eps trouve " + str(eps))
    #print (LM)



    return order_type(LM,LT,MCoeff_copy,eps)
    
