import numpy as np
import time
import data_structure as ds
import lpt
import SchedJuxtapose
import lpt_typed
import order_type
import order_type_greedy
import order_type_trick
import greedy_clust_with_lpt_typed
import greedy_cluster_
import PTAS

'''
McoeffId2 =np.array([[1.0, 1.0],
                     [1.0, 1.0]])

McoeffId3 =np.array([[1.0, 1.0, 1.0],
                     [1.0, 1.0, 1.0],
                     [1.0, 1.0, 1.0]])

McoeffId5 =np.array([[1.0, 1.0, 1.0, 1.0, 1.0],
                     [1.0, 1.0, 1.0, 1.0, 1.0],
                     [1.0, 1.0, 1.0, 1.0, 1.0],
                     [1.0, 1.0, 1.0, 1.0, 1.0],
                     [1.0, 1.0, 1.0, 1.0, 1.0]])


McoeffId = McoeffId2
'''

Mcoeffdiff = np.array([[1.00, 0.16, 1.83, 0.33, 1.66],
                       [0.16, 1.00, 0.50, 1.50, 0.66],
                       [1.83, 0.50, 1.00, 1.33, 0.83],
                       [0.33, 1.50, 1.33, 1.00, 1.16],
                       [1.66, 0.66, 0.83, 1.16, 1.00]])

MCoeff = Mcoeffdiff




def lpt_makespan(nbLM, LT):
    LM = ds.create_LM(nbLM)
    LML = lpt.lpt(LM, LT)
    return lpt.final_cost_LM_1type(LML)

def juxtapose_makespan(nbLM, LT):
    LM = ds.create_LM(nbLM)
    LMJ = SchedJuxtapose.SchedJuxtapose(LM, LT)
    return lpt.final_cost_LM_1type(LMJ)

def lpt_type_makespan(nbLM, LT):
    LM = ds.create_LM(nbLM)
    LML = lpt_typed.lpt_typed(LM,LT,McoeffId)
    return lpt.final_cost_LM_1type(LML)

def cluster_with_lpt_makespan(nbLM, LT):
    LM = ds.create_LM(nbLM)
    LMC = greedy_clust_with_lpt_typed.greedy_clust_final_with_lpt_typed(LM, LT, McoeffId, 0.001)
    #ds.affichage_lm(LMC, nbLM)
    return lpt.final_cost_LM_1type(LMC)

def cluster_without_lpt_makespan(nbLM, LT):
    LM = ds.create_LM(nbLM)
    LMC = greedy_cluster_.greedy_clust_final_V2_wo_lpt_typed(LM, LT, McoeffId)
    #ds.affichage_lm(LMC, nbLM)
    return lpt.final_cost_LM_1type(LMC)

def order_type_makespan(nbLM, LT):
    LM = ds.create_LM(nbLM)
    LMO = order_type.order_type_final(LM, LT, McoeffId)
    return lpt.final_cost_LM_1type(LMO)







def lpt_cost_max(nbLM, LT, Mcoeff):
    LM = ds.create_LM(nbLM)
    LML = lpt.lpt(LM, LT)
    return ds.cost_max(LML, LT, Mcoeff)

def lpt_typed_cost_max(nbLM,LT,MCoeff):
    LM = ds.create_LM(nbLM)
    LMLT = lpt_typed.lpt_typed(LM,LT,MCoeff)
    return ds.cost_max(LMLT,LT,MCoeff)

def juxtapose_cost_max(nbLM, LT, Mcoeff):
    LM = ds.create_LM(nbLM)
    LMJ = SchedJuxtapose.SchedJuxtapose(LM, LT, Mcoeff)
    return ds.cost_max(LMJ, LT, Mcoeff)

def cluster_with_lpt_cost_max(nbLM, LT, Mcoeff):
    LM = ds.create_LM(nbLM)
    LMC = greedy_clust_with_lpt_typed.greedy_clust_final_with_lpt_typed(LM, LT, Mcoeff, 0.001)
    return ds.cost_max(LMC, LT, Mcoeff)

def cluster_without_lpt_cost_max(nbLM, LT, Mcoeff):
    LM = ds.create_LM(nbLM)
    LMC = greedy_cluster_.greedy_clust_final_wo_lpt_typed(LM, LT, Mcoeff)
    return ds.cost_max(LMC, LT, Mcoeff)

def order_type_cost_max(nbLM, LT, Mcoeff):
    LM = ds.create_LM(nbLM)
    LMO = order_type.order_type_final(LM, LT, Mcoeff)
    return ds.cost_max(LMO,LT, Mcoeff)

def order_type_greedy_cost_max(nbLM, LT, Mcoeff):
    LM = ds.create_LM(nbLM)
    LMO = order_type_greedy.order_type_final(LM, LT, Mcoeff)
    return ds.cost_max(LMO, LT, Mcoeff)

def order_type_trick_cost_max(nbLM, LT, Mcoeff):
    LM = ds.create_LM(nbLM)
    LMO = order_type_trick.order_type_final(LM, LT, Mcoeff)
    return ds.cost_max(LMO, LT, Mcoeff)

def ptas_cost_max(nbLM, LT, Mcoeff):
    LM = ds.create_LM(nbLM)
    LMP = PTAS.PTAS(LM, LT, Mcoeff, 5)
    return ds.cost_max(LMP, LT, Mcoeff)


def ptas_time(LM, LT, Mcoeff, k):
    start_time = time.time()
    PTAS.PTAS(LM, LT, Mcoeff, k,grouped=False)
    t = time.time() - start_time
    print("k = ", k, "---  %s seconds\n" % t)
    return t


'''def cluster_greedy_cost_max(nbLM, LT, Mcoeff):
    LM = ds.create_LM(nbLM)
    LMC = cluster_greedy.greedy_clust_final(LM,LT,Mcoeff)
    return ds.cost_max(LMC, LT, Mcoeff)'''


def lpt_typed_diff_cost_max(nbLM, LT, Mcoeff):
    LM = ds.create_LM(nbLM)
    LMT = lpt_typed.lpt_typed_difference(LM, LT, Mcoeff)
    return ds.cost_max(LMT, LT, Mcoeff)

def lpt_typed_faster_cost_max(nbLM, LT, Mcoeff):
    LM = ds.create_LM(nbLM)
    LMT = lpt_typed.lpt_typed_faster(LM, LT, Mcoeff)
    return ds.cost_max(LMT, LT, Mcoeff)









def lpt_time(LM, nbLT):
    start_time = time.time()
    LT = ds.create_LT(nbLT, 5, 100)
    lpt.lpt(LM, LT)
    t = time.time() - start_time
    #print("nbLT = ", nbLT, "---  %s seconds\n" % t)
    return t


Mcoeffdiff = np.array([[1.00, 0.16, 1.83, 0.33, 1.66],
                       [0.16, 1.00, 0.50, 1.50, 0.66],
                       [1.83, 0.50, 1.00, 1.33, 0.83],
                       [0.33, 1.50, 1.33, 1.00, 1.16],
                       [1.66, 0.66, 0.83, 1.16, 1.00]])
MCoeff = Mcoeffdiff
def order_time(LM, nbLT):
    start_time = time.time()
    LT = ds.create_LT(nbLT, 5, 100)
    order_type.order_type_final(LM,LT,MCoeff)
    t = time.time() - start_time
    #print("nbLT = ", nbLT, "---  %s seconds\n" % t)
    return t




Mcoeff1=np.array([ [1.0,  1.0],
                   [1.0, 1.0]])
def jux_time(LM, nbLT):
    start_time = time.time()
    LT = ds.create_LT(nbLT, 5, 100)
    SchedJuxtapose.SchedJuxtapose(LM, LT, Mcoeff1)
    t = time.time() - start_time
    #print("nbLT = ", nbLT, "---  %s seconds\n" % t)
    return t


def cluster_wo_time(LM, nbLT):
    start_time = time.time()
    LT = ds.create_LT(nbLT, 5, 100)
    greedy_cluster_.greedy_clust_final_wo_lpt_typed(LM, LT, MCoeff)
    t = time.time() - start_time
    #print("nbLT = ", nbLT, "---  %s seconds\n" % t)
    return t


def LPT_typed_time(LM, nbLT):
    start_time = time.time()
    LT = ds.create_LT(nbLT, 5, 100)
    lpt_typed.lpt_typed(LM, LT, MCoeff)
    t = time.time() - start_time
    #print("nbLT = ", nbLT, "---  %s seconds\n" % t)
    return t
