import copy
from operator import itemgetter
import data_structure


def final_cost_inlist(C_old, new_cost, pos):
    """
        returns the final cost of a cost's list changing on pos the old cost with the new_cost
    """
    C_old_copy = copy.deepcopy(C_old)
    C_old_copy[pos] = new_cost
    return max(C_old_copy)


def lpt_typed(LM, LT, MCoeff, group=False, k = 0):
    """input : list of machines * list of tasks * Matrix Coefficient tasks
        output : a new list of machines after using algorithm

        This algorithm works like lpt in the first place
        but it is not looking for the machine with the minimal cost to add a task
        rather it looks for the machine that will be the least affected after adding a task
    """

    # a new list sorted in a decreasing tasks' size
    LT_sorted = sorted(LT, key=itemgetter('size'), reverse=True)
    LM_lpt_typed = copy.deepcopy(LM)

    # operating in all tasks
    for i in range(0, len(LT)):
        # if there's an index i in LM and  the machine is empty, add the task in the machine
        if ((i < len(LM)) and len(LM_lpt_typed[i]['LTM']) == 0):
            LM_lpt_typed[i]['LTM'].append(LT_sorted[i])
        # we will put the task in the machine that will cost the least after adding it
        else:
            # C_tmp is a list that will contain all machine's cost after adding the current task
            C_tmp = []
            # C_old is a list containing all machine's cost before adding the current task
            C_old = []
            for k in range(len(LM_lpt_typed)):
                LM_lpt_typed_copy = copy.deepcopy(LM_lpt_typed)
                C_old.append(data_structure.cost_M_gen(LM_lpt_typed_copy[k], MCoeff))
                
            # operating in all machines
            for j in range(len(LM_lpt_typed)):
                # operating in a copy so we don't affect what we want to return : LM_lpt_typed
                LM_lpt_typed_copy = copy.deepcopy(LM_lpt_typed)
                # putting the task in the temporary LM
                LM_lpt_typed_copy[j]['LTM'].append(LT_sorted[i])
                # calculating the final cost of LM after adding the task
                C_tmp.append(final_cost_inlist(C_old, data_structure.cost_M_gen(LM_lpt_typed_copy[j], MCoeff), j))
            # adding the task in the machine that will cost the least afterwards
            LM_lpt_typed[C_tmp.index(min(C_tmp))]['LTM'].append(LT_sorted[i])

    return LM_lpt_typed


def lpt_typed_difference(LM,LT,MCoeff, group=False, k = 0):
    """input : list of machines * list of tasks * Matrix Coefficient tasks
        output : a new list of machines after using algorithm

        This algorithm works like lpt in the first place
        but it is not looking for the machine with the minimal cost to add a task
        rather it looks for the machine that will be the least affected after adding a task
        this one looks the minimal differences between the old and the new one

        THIS ONE IS NOT BETTER THAN THE OLD ONE
        Although from time to times coupled with PTAS the cost_max is reduced, don't ask me why
    """

    #a new list sorted in a decreasing tasks' size
    LT_sorted = sorted(LT,key=itemgetter('size'),reverse=True)
    LM_lpt_typed = copy.deepcopy(LM)

    #operating in all tasks
    for i in range(0,len(LT)):
        #if there's an index i in LM and  the machine is empty, add the task in the machine
        if ((i<len(LM)) and len(LM_lpt_typed[i]['LTM'])==0):
            LM_lpt_typed[i]['LTM'].append(LT_sorted[i])

        #we will put the task in the machine that will cost the least after adding it
        else:
            """will put the task in the machine where : new_cost_machine - old_cost_machine , is minimal
                looking machine by machine, faster but not the best
            """
            #C_before is a list contains all machine's cost before adding the current task
            C_before=[]
            for k in range(len(LM_lpt_typed)):
                C_before.append(data_structure.cost_M_gen(LM_lpt_typed[k],MCoeff))

            #C_after_diff is list that will contain the difference of a machine's cost after and before adding the task
            C_after_diff=[]

            #operating in all machines
            for j in range(len(LM_lpt_typed)):
                #operating in a copy so we don't affect what we want to return : LM_lpt_typed
                LM_lpt_typed_copy=copy.deepcopy(LM_lpt_typed)
                LM_lpt_typed_copy[j]['LTM'].append(LT_sorted[i])
                C_after_diff.append(data_structure.cost_M_gen(LM_lpt_typed_copy[j],MCoeff)-C_before[j])
            #adding the task in the machine that will cost the least afterwards
            LM_lpt_typed[C_after_diff.index(min(C_after_diff))]['LTM'].append(LT_sorted[i])

    return LM_lpt_typed

    
#==============================================================================
#  main
#==============================================================================
"""
nb_types=3
nb_tasks=50
max_weight=20
nb_machines=2

LT=data_structure.create_LT(nb_tasks,nb_types,max_weight)
MCoeff=data_structure.create_A_alpha(nb_types,nb_types)
LM=data_structure.create_LM(nb_machines)

LM_lpt_typed = lpt_typed(LM,LT,MCoeff,True)
data_structure.print_lm(LM_lpt_typed,nb_machines)
print("lpt_typed cost : ")
print(data_structure.cost_final_LM_gen(LM_lpt_typed,MCoeff))
"""
