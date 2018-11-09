#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 11:29:16 2018

@author: 3531662
"""

import copy
import math
# Divers imports
import data_structure
import lpt_typed
from operator import itemgetter
import greedy_cluster_tools


# ==============================================================================
# greedy_cluster with lpt typed
# ==============================================================================

# allocates tasks from clusters
def greedy_cluster_with_lpt_typed(LM, LT, MCoeff, esp):
    """ input : List of machines, List of tasks, Array of coefficients, Double for the coefficient*LB wanted
        output : new List of mahines
        builds clusters of tasks depending on their types. Then allocates those tasks with the LB criteria
    """

    LB = greedy_cluster_tools.borne_inf(LT, LM)
    LC = []

    # create list of types
    All_types = []
    for task in LT:
        if (task['type'] not in All_types):
            All_types.append(task['type'])

    # getting type clustered
    LC = greedy_cluster_tools.rec_clusterize(LC, All_types, MCoeff)
    # LC_rec_clusterize_improved(LC,All_types,MCoeff)

    # create clusters of tasks LT_clusterized based on clusters of types LC
    LT_clusterized = [[] for cluster in range(len(LC))]
    for cluster in range(len(LC)):
        for task in LT:
            if task['type'] in LC[cluster]:
                LT_clusterized[cluster].append(task)

    # allocate clusterized tasks LT_clusterized in machines LM so as not to surpass LB
    # here we'll operate first in the cluster : cluster, then in the tasks in that cluster : task, --> two loops
    # all of that operating in parallel with a machine : num_machine, it is not embodied by a loop
    num_machine = 0
    machine_done = False

    LM_greedy = copy.deepcopy(LM)
    LT_clust_copy = copy.deepcopy(LT_clusterized)

    # operating in clusters containing tasks, looping in a copy to avoid weird bugs
    for cluster in LT_clust_copy:
        # if we are still operating in an existing machine
        if num_machine < len(LM_greedy):
            # if the cluster is not empty
            if len(cluster):
                # sort decreasingly by tasks' size in the cluster
                cluster = sorted(cluster, key=itemgetter('size'), reverse=True)

            cluster_copy = copy.deepcopy(cluster)
            # operating task in that cluster, looping in a copy to avoid weird bugs, but operating directly in results : LM_greedy
            for task in cluster_copy:
                # if we are still operating in an existing machine
                if num_machine < len(LM_greedy):
                    # add temporarily the task in the num_machine
                    (LM_greedy[num_machine]['LTM']).append(task)
                    cluster.remove(task)

                    # if the num_machine have now a cost > esp*LB
                    if (data_structure.cost_M_gen(LM_greedy[num_machine], MCoeff) > esp * LB):
                        # we remove the added task and num_machine is done
                        cluster.append(task)
                        del LM_greedy[num_machine]['LTM'][-1]
                        machine_done = True

                    if machine_done:
                        num_machine += 1
                        # add the task in the next existing machine
                        if num_machine < len(LM_greedy):
                            (LM_greedy[num_machine]['LTM']).append(task)
                            cluster.remove(task)
                            machine_done = False

                        # case bad_esp :
                        else:
                            LM_greedy = lpt_typed.lpt_typed(LM_greedy, [task], MCoeff)
                            cluster.remove(task)
                            machine_done = False

                # case bad_esp
                else:
                    LM_greedy = lpt_typed.lpt_typed(LM_greedy, [task], MCoeff)
                    cluster.remove(task)
        # case bad_esp
        else:
            cluster_copy = copy.deepcopy(cluster)
            for task in cluster_copy:
                LM_greedy = lpt_typed.lpt_typed(LM_greedy, [task], MCoeff)
                cluster.remove(task)

    return LM_greedy




def greedy_clust_best_eps_with_lpt_typed(LM, LT, MCoeff, eps_precision=0.1):
    """input : list of machines * list of tasks * matrix types'coefficient * precision of eps i.e. 1.1 ? or 1.01 ? etc (by default : 0.1)
        output : the best eps that respect the following condition - all machine's cost must be < eps*LB

        This function uses dichotomy to find the best eps
    """
    # variables needed to dichotomize
    end_eps = float(2.0)
    start_eps = float(0.0)
    min_makespan = data_structure.cost_final_LM_gen(greedy_cluster_with_lpt_typed(LM, LT, MCoeff, end_eps), MCoeff)

    # until eps' precision is not the one wanted
    while ((math.fabs(end_eps - start_eps) > eps_precision)):
        # storing the (list of machines)'s cost when eps is the midpoint of start_eps and end_eps
        A = data_structure.cost_final_LM_gen(
            greedy_cluster_with_lpt_typed(LM, LT, MCoeff, (float)(math.fabs(end_eps + start_eps)) / 2.0), MCoeff)

        # the cost is not better than the actual one, i.e. eps cannot be below the midpoint
        if (A > min_makespan):
            # therefore we set the midpoint as the new start_eps
            start_eps = (float)(math.fabs(end_eps + start_eps)) / 2.0

        # the cost is better, i.e. eps can be below the midpoint
        else:
            min_makespan = A
            end_eps = (float)(math.fabs(end_eps + start_eps)) / 2.0
    # finally we calculate which one between start_eps and end_eps holds the best eps
    # certainly the precision is the wanted one, but nothing says if the (list of machines)'s cost is lower with start_eps or end_eps
    if data_structure.cost_final_LM_gen(greedy_cluster_with_lpt_typed(LM, LT, MCoeff, start_eps),
                                        MCoeff) > data_structure.cost_final_LM_gen(
            greedy_cluster_with_lpt_typed(LM, LT, MCoeff, end_eps), MCoeff):
        return end_eps
    return start_eps





def greedy_clust_final_with_lpt_typed(LM, LT, MCoeff, eps_precision=0.01, k = 0 ):
    """input : list of machines * list of tasks * matrix types'coefficient * precision of eps i.e. 1.1 ? or 1.01 ? etc (by default : 0.0001)
        output : a new list of machines

        Returns the best arrangement for a list of tasks in a list of machines by using greed_clust algorithm
    """
    eps = greedy_clust_best_eps_with_lpt_typed(LM, LT, MCoeff, eps_precision)
    return greedy_cluster_with_lpt_typed(LM, LT, MCoeff, eps)



