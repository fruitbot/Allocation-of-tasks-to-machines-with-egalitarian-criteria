#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import copy
"""
General tools for greedy_cluster stuffs
"""

def borne_inf(LT, LM):
    """returns borne_inf LB for makespan
        makespan is such that LB <= makespan <= 2LB
    """
    #max_task = max(LT[]['size'])
    max_task = max(task['size'] for task in LT)
    av = sum(task['size'] for task in LT)/len(LM)
    return max(max_task, av) 


def compatible_types(t1,t2,A_alpha):
    """ True if t1 and t2 are compatible
    """
    return float(A_alpha[t1-1][t2-1])<=1




def rec_clusterize(LC_rec,All_types,A_alpha):
    """recursive function to get clusters, not the perfect one though
    """
    
    if (len(All_types)==0):
        #all types have been added to a cluster
        return LC_rec

    if (len(LC_rec)==0):
        #no types have been added to a cluster
        LC_rec.append([All_types[0]])
        All_types.remove(All_types[0])
        return rec_clusterize(LC_rec,All_types,A_alpha)

    
    All_copy=list(All_types) #copy All_types to avoid a bug in the first for : 
                             #which tested if j was still in All_types but it was at some point removed from it -> problem
    if (len(LC_rec)!=0):
        #there is a cluster, in the following we want to add all other compatible types with the cluster
        for j in All_copy:
            #j is all the remaining types that are not yet in a cluster
            bool_temp=1
            for i in LC_rec[0]:
                #i is all the types that are found in the current cluster 
                if not compatible_types(i,j,A_alpha):
                    bool_temp=0
            if (bool_temp==1 and j not in LC_rec[0]):
                LC_rec[0].append(j)
                All_types.remove(j)

    #LC_rec is the cluster created and with rec_clusterize([],All_types,A_alpha) we will create anoother cluster and so on
    return LC_rec+rec_clusterize([],All_types,A_alpha)
    

    
def rec_clusterize_improved(LC_rec,All_types,A_alpha):
    """recursive function to get clusters, not the perfect one though
        This function needs some real change (i.e. milk)
    """
    if (len(All_types)==0):
        #all types have been added to a cluster
        return LC_rec

    if (len(LC_rec)==0):
        #no types have been added to a cluster
        LC_rec.append([All_types[0]])
        All_types.remove(All_types[0])
        return rec_clusterize_improved(LC_rec,All_types,A_alpha)



    
    if (len(LC_rec)!=0):
        n=len(All_types)
        for nb_tour in range(n):
            All_types_copy=list(All_types) #copy All_types to avoid a bug in the first for : 
                                           #which tested if j was still in All_types but it was at some point removed from it -> problem
            LC_rec_copy=copy.deepcopy(LC_rec)
            
            #oprating in copies : there is a cluster, in the following we want to add all other compatible types with the cluster
            for j in All_types_copy:
                #j is all the remaining types that are not yet in a cluster
                bool_temp=1
                for i in LC_rec_copy[0]:
                    #i is all the types that are found in the current cluster 
                    if not compatible_types(i,j,A_alpha):
                        bool_temp=0
                if (bool_temp==1 and j not in LC_rec_copy[0] and j not in LC_rec[0]):
                    LC_rec_copy[0].append(j)
                    All_types_copy.remove(j)
            
            #operating in results, no longer in copies
            if (len(LC_rec_copy[0])>1):
                L_temp = []
                #comparing with the first type in the cluster although it should be with everyone.. HAVE TO CHANGE
                [L_temp.append(A_alpha[LC_rec_copy[0][0]-1][i-1]) for i in LC_rec_copy[0]]
                ind = LC_rec_copy[0][L_temp.index((min(L_temp)))]
                if (ind not in LC_rec[0]):
                    LC_rec[0].append(ind)
                    All_types.remove(ind)
                
    #LC_rec is the cluster created and with rec_clusterize([],All_types,A_alpha) we will create anoother cluster and so on
    return LC_rec + rec_clusterize_improved([],All_types,A_alpha)