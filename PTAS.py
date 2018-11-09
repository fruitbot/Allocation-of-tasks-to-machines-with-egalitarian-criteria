"""
Importing libraries
"""
import data_structure
import copy
import lpt_typed
from operator import itemgetter
import sys
import lpt
import numpy as np

"""
Functions
"""


def prep_for_PTAS(LM, LT, MCoeff, k, current_lowest_cost_max, current_best_LM):
    """
    ARGUMENTS
        List of machines * List of Tasks * Array coefficient * k first biggest tasks * List of size 1 containing cost_max * List containing a LM
        e.g. : current_lowest_cost_max = [50], it is like so in order to have a pointer effect
                same for current_best_LM

    ALGORITHM
        preparation for Polynomial-time approximation scheme algorithm
        This is algorithm works by following branches in a tree :
            looping and calling itself in the loops so we can have something like this :

                for
                    for
                        for

            See it like a tree of height k and for each level there's nb_machines branches where you can put your task
            number of for = k biggest tasks
            loop's lentgh = nb_machines

        Returns nothing, passes the result in argument current_best_LM

    COMPLEXITY
        nb_machines ** k biggest tasks
        nb_machines ^ k
        len(LM) raised to k

    N.B. :
            only PTAS shall call this function

            in order to run properly
                --current_lowest_cost_max have to be initialize by putting all k tasks into one machine then calculate its cost
            No problemo returning nothing since it's used in PTAS
    """

    # calculates the cost_max of LM --- the branch and bound technique : cutting the branch when the cost is already bigger than the current_lowest_cost
    if isinstance(LT, np.ndarray):
        cost = lpt.final_cost_LM_1type(LM)
    else: cost = data_structure.cost_final_LM_gen(LM, MCoeff)
    if (cost >= current_lowest_cost_max[0]):  # the previous added task makes things worse so we abort/cut this branch
        # branch cutted
        return

        # the following test is after the cost test because we want to avoid leafs that are useless
    # verify if there's still tasks to add
    if (k == 0):  # no more big tasks to add
        if (cost != 0):  # useful when we first enter this function
            # lowest cost change and put LM into the current_best_LM
            current_lowest_cost_max[0] = cost
            current_best_LM[0] = copy.deepcopy(LM)  # copy otherwise the last task is not added
        # else : lowest cost NOT changed doesn't change
        return

        # as always create copies to avoid unwanted bugs
    if isinstance(LT, np.ndarray):
        LT_copy_sorted = sorted(LT, reverse=True)
    else: LT_copy_sorted = sorted(LT, key=itemgetter('size'), reverse=True)
    LM_copy = copy.deepcopy(LM)

    # loopings
    for num_machine in range(0, len(LM)):
        if (len(LT) != 0):
            task_temp = LT_copy_sorted[0]
            # put the task in the num_machine-th machine in LM_copy
            (LM_copy[num_machine]['LTM']).append(task_temp)

            # take out the task in LT_copy
            LT_copy_sorted.remove(task_temp)

            # call itself  and in argument decrease k by 1
            prep_for_PTAS(copy.deepcopy(LM_copy), LT_copy_sorted, MCoeff, k - 1, current_lowest_cost_max, current_best_LM)

            
            # put the task back in LT_copy
            LT_copy_sorted.insert(0, task_temp)

            # take out the task in LM_copy
            (LM_copy[num_machine]['LTM']).remove(task_temp)

    return

    


def PTAS(LM, LT, MCoeff, k,grouped=False):
    """
    ARUGMENTS
        List of machines * List of Tasks * Array coefficient * k first biggest tasks

    ALGORITHM
        Polynomial-time approximation scheme algorithm

        use prep_for_PTAS for the k biggest tasks LM
        put the remaining tasks using the lpt-typed method in LM

        Returns a NEW LM

    COMPLEXITY
        lpt_typed complexity or prep_for_PTAS

    N.B. :
            to function properly please insert a low value for k otherwise be patient and be exponential
    """
    print(type(LT))
    if isinstance(LT, np.ndarray):
        LT_copy_sorted_temp = sorted(LT, reverse=True)
    else: LT_copy_sorted_temp = sorted(LT, key=itemgetter('size'), reverse=True)

    # case where k <= m
    if k <= len(LM):
        # one task per machine
        current_best_LM = [copy.deepcopy(LM)]
        for i in range(k):
            print(i)
            try:
                current_best_LM[0][i]['LTM'].append(LT_copy_sorted_temp[i])
            except:
                print(current_best_LM, k, len(LT))
                sys.exit(1)

    else: # use prep_PTAS
        #   initializes the needed stuffs i.e.   current_lowest_cost_max
        # all below is done in a temp, putting all tasks in one machine to initialize supra
        current_best_LM = [copy.deepcopy(LM)]
        LM_copy_temp = copy.deepcopy(LM)
        for i in range(0, k):
            if (len(LT_copy_sorted_temp) != 0):
                tmp_task = LT_copy_sorted_temp[0]
                (LM_copy_temp[0]['LTM']).append(tmp_task)
                LT_copy_sorted_temp.remove(tmp_task)
        # after this, it is initialized =)
        if isinstance(LT, np.ndarray):
            current_lowest_cost_max = [lpt.final_cost_LM_1type(LM)]
        else: current_lowest_cost_max = [data_structure.cost_final_LM_gen(LM_copy_temp, MCoeff)]

        #   finding the optimal, the best way to put the k biggest task in LM calling prep_for_PTAS
        if (k>len(LT)):
            k=len(LT)
        prep_for_PTAS(LM, LT, MCoeff, k, current_lowest_cost_max, current_best_LM)


        #   using lpt_typed for the remaining tasks

    # removing the k biggest tasks in LT_copy_sorted
    if isinstance(LT, np.ndarray):
        LT_copy_sorted = sorted(LT, reverse=True)
    else: LT_copy_sorted = sorted(LT, key=itemgetter('size'), reverse=True)
    for i in range(k):
        if (len(LT_copy_sorted)!=0):
            LT_copy_sorted.pop(0)

    # calling lpt_typed with the LM returned by prep_for_PTAS and LT_copy_sorted
    #return lpt_typed.lpt_typed(current_best_LM[0], LT_copy_sorted, MCoeff,grouped)
    return lpt.lpt(current_best_LM[0], LT_copy_sorted, MCoeff)


def PTAS_difference(LM,LT,MCoeff,k, group=False):
    """
    ARUGMENTS
        List of machines * List of Tasks * Array coefficient * k first biggest tasks

    ALGORITHM
        Polynomial-time approximation scheme algorithm

        use prep_for_PTAS for the k biggest tasks LM
        put the remaining tasks using the lpt-typed_difference method in LM

        Returns a NEW LM

    COMPLEXITY
        lpt_typed complexity or prep_for_PTAS

    N.B. :
            to function properly please insert a low value for k otherwise be patient and be exponential
    """
    LT_copy_sorted_temp = sorted(LT,key = itemgetter('size'),reverse=True)

    # case where k <= m
    if k <= len(LM):
        print("little")
        # one task per machine
        current_best_LM = [copy.deepcopy(LM)]
        for i in range(k):
            try:
                current_best_LM[0][i]['LTM'].append(LT_copy_sorted_temp[i])
            except:
                print(current_best_LM, k, len(LT))
                sys.exit(1)


    else: # use prep_PTAS

        #   tinitializes the needed stuffs i.e.   current_lowest_cost_max
        #all below is done in a temp, putting all tasks in one machine to initialize supra
        current_best_LM=[copy.deepcopy(LM)]
        LM_copy_temp = copy.deepcopy(LM)
        for i in range(0,k):
            if(len(LT_copy_sorted_temp)!=0):
                tmp_task=LT_copy_sorted_temp[0]
                (LM_copy_temp[0]['LTM']).append(tmp_task)
                LT_copy_sorted_temp.remove(tmp_task)
        #after this, it is initialized =)
        if isinstance(LT, np.ndarray):
            current_lowest_cost_max = [lpt.final_cost_LM_1type(LM)]
        else: current_lowest_cost_max = [data_structure.cost_final_LM_gen(LM_copy_temp, MCoeff)]

        #   finding the optimal, the best way to put the k biggest task in LM calling prep_for_PTAS
        if (k>len(LT)):
            k=len(LT)    
        prep_for_PTAS(LM,LT,MCoeff,k,current_lowest_cost_max,current_best_LM)


    #   using lpt_typed for the remaining tasks

    #removing the k biggest tasks in LT_copy_sorted
    LT_copy_sorted = sorted(LT,key = itemgetter('size'),reverse=True)
    for i in range(k):
        if (len(LT_copy_sorted)!=0):
            LT_copy_sorted.pop(0)

    #calling lpt_typed with the LM returned by prep_for_PTAS and LT_copy_sorted
    #return lpt_typed.lpt_typed_difference(current_best_LM[0],LT_copy_sorted,MCoeff,group)
    return lpt.lpt(current_best_LM[0], LT_copy_sorted, MCoeff)




#==============================================================================
# MAIN
#==============================================================================
"""
nb_machines=3
nb_types=4
nb_taches=10
LM = data_structure.create_LM(nb_machines)
LT = data_structure.create_LT(nb_taches,nb_types,100)
MCoeff =data_structure.create_A_alpha(nb_types,100)

#PTAS_original
LM_ptas_original=PTAS(LM,LT,MCoeff,20,True)
data_structure.print_lm(LM_ptas_original,nb_machines)
print(data_structure.cost_final_LM_gen(LM_ptas_original,MCoeff),"\n")
#PTAS_faster
LM_ptas_faster=PTAS_faster(LM,LT,MCoeff,5)
data_structure.print_lm(LM_ptas_faster,nb_machines)
print(data_structure.cost_final_LM_gen(LM_ptas_faster,MCoeff),"\n")

#PTAS_difference
LM_ptas_difference=PTAS_difference(LM,LT,MCoeff,3)
data_structure.print_lm(LM_ptas_difference,nb_machines)
print(data_structure.cost_final_LM_gen(LM_ptas_difference,MCoeff),"\n")

#lpt_typed_original
LM_typed_original=lpt_typed.lpt_typed(LM,LT,MCoeff)
data_structure.print_lm(LM_typed_original,nb_machines)
print(data_structure.cost_final_LM_gen(LM_typed_original,MCoeff),"\n")

#lpt_typed_faster
LM_typed_faster=lpt_typed.lpt_typed_faster(LM,LT,MCoeff)
data_structure.print_lm(LM_typed_faster,nb_machines)
print(data_structure.cost_final_LM_gen(LM_typed_faster,MCoeff),"\n")

#lpt_typed_difference
LM_typed_diffrence=lpt_typed.lpt_typed_difference(LM,LT,MCoeff)
data_structure.print_lm(LM_typed_diffrence,nb_machines)
print(data_structure.cost_final_LM_gen(LM_typed_diffrence,MCoeff),"\n")


    
data_structure.verif_tasks(LM_ptas_original,LT)
data_structure.verif_tasks(LM_ptas_faster,LT)
data_structure.verif_tasks(LM_ptas_difference,LT)
data_structure.verif_tasks(LM_typed_original,LT)
data_structure.verif_tasks(LM_typed_faster,LT)
data_structure.verif_tasks(LM_typed_diffrence,LT)"""