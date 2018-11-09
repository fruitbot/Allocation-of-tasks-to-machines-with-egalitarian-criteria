import numpy as np
import data_structure
import copy
import math
import data_structure
from operator import itemgetter 

# returns borne_inf LB for makespan
# makespan is such that LB <= makespan <= 2LB
def borne_inf(LT, LM, MCoeff):
    #max_task = max(LT[]['size'])
    max_task = max(task['size'] for task in LT)
    av = sum(task['size'] for task in LT)/len(LM)
    return max(max_task, av)


def  order(All_types, MCoeff):

    ordered_types = []
    # get first 2 types, so that 2 most compatible types are together
    best = np.unravel_index(MCoeff.argmin(), MCoeff.shape)
    
    # neutralise diagonal
    for i in range(len(All_types)):
        MCoeff[i][i] = float('Inf')

    # get types involved in best
    # decide who really is the first type between both in best and remove it from All_type

    minimum = float(min(MCoeff[best[0]]))
    x = best[0]
    y = MCoeff[best[0]].argmin()

    if float(min(MCoeff[best[1]])) < minimum:
        x = best[1]
        minimum = min(MCoeff[best[1]])
        y = MCoeff[best[1]].argmin()

    MCoeff[:,x] = float('Inf')
    # uncomment if clusters wanted
    """ordered_types.append([x+1])
    ordered_types.append([y+1])"""

    try:
        ordered_types.append(x+1)
        ordered_types.append(y+1)
        All_types.remove(x+1)
        All_types.remove(y+1)
        x = y
    except ValueError:
        print ("Le bug a lieu pour l'instance :")
        print (All_types)
        print (MCoeff)
        return

    while All_types:
        # find next type that fits best to type x + 1
        if len(All_types) == 1: # if there is only one type left
            # uncomment if clusters wanted:
            """ordered_types.append(All_types)"""
            ordered_types.extend(All_types)
            break
        # get bet fit y for x and treat it
        y = MCoeff[x].argmin()
        # uncomment if clusters wanted
        """if MCoeff[x][y] > 1:
            ordered_types.append([y+1])
        else : ordered_types.append([y+1])"""
        ordered_types.append(y+1)
        All_types.remove(y+1)
        MCoeff[:,x] = float('Inf') # neutralised the alredy treated couple
        x = y

        # amelioration possible = clusters lorsque coeff > 1
    return ordered_types
    

def order_type(LM, LT, MCoeff,esp):
    """ input : List of machines, List of tasks, Array of coefficients, Double for the coefficient*LB wanted
        output : List of mahines
        order type depending on Mcoeff
        then allocate tasks with the LB criteria
        not very good if types are compatible: because all coeffs on a machine will be 1 while they could be less if mixed
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
                if ((data_structure.cost_M_gen(LM[machine], MCoeff)) > esp ):
                    #print ("cost " + str(data_structure.cost_M_gen(LM[machine], MCoeff)))
                    #print ("esp LMB " + str(esp) + " " + str(LB) + " " + str(esp*LB))
                    # remove task from machine and put it in the next one
                    #print  ("remove task from machine and put it in the next one")
                    LM[machine]['LTM'] = sorted(LM[machine]['LTM'] , key = itemgetter('size'), reverse=True)
                    machine += 1

                    if (machine == len(LM)):
                        return 0

                    LM[machine]['LTM'].append(task)


    # cas ou il reste des machines libres
    for machine in range(len(LM)):

        if not LM[machine]["LTM"]: # this machine is empty 

            # try to fit tasks from the most charged machine(s) on the empty machine
            most_charged = data_structure.max_ind_cost_LM_gen(LM, MCoeff)
            
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

    #variables needed to dichotomize
    start_eps, end_eps = data_structure.inf_sup_types(LT, LM, MCoeff)
    
    # until eps' precision is not the one wanted
    while((math.fabs(end_eps - start_eps) > eps_precision)):
        # storing the (list of machines)'s cost when eps is the midpoint of start_eps and end_eps
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
    All_types = list(range(1, len(MCoeff) + 1))


    # order types
    global ordered_types # glabal because connot be added as argument. And we dont want order() to be called all the time!
    ordered_types = order(All_types, copy.deepcopy(MCoeff))

    eps_precision=0.01
    MCoeff_copy = copy.deepcopy(MCoeff)
    LM_copy = copy.deepcopy(LM)
    eps = order_type_best_eps(LM_copy,LT,MCoeff_copy,eps_precision)

    return order_type(LM,LT,MCoeff_copy,eps)
