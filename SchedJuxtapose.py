import data_structure as ds
import lpt
import numpy as np
import PTAS


'''#############################################################################################'''
'''                                             Juxtapose                                       '''
'''#############################################################################################'''
# SchedJuxtapose
'''
This fonction cuts the sequence of tasks of 2 types into m sub-sequences. 
There are (m-1) cut points so that all the possible subsequences are generated(as combinations).
Juxtapose aims to find the minimal cost matching between LT1 et LT2.
'''

# dictionary of tasks looks like: [{"type": 1, "size": 80}, {"type": 2, "size": 50}...]


def LTCutinTwo(LT):
    LT_tmp = LT
    LT1=[]
    LT2=[]
    for elt in LT_tmp:
        if elt['type'] == 1:
            LT1.append(elt)
        elif elt['type'] == 2:
            LT2.append(elt)
    return LT1, LT2


def PermutationGenerator(m):
    """Generating all possible combinations of machines: (M1, M2)"""
    nb = m
    Perm = []
    for i in range (1, nb):
        Perm.append([i, nb-i])
    #print(np.matrix(Perm))
    return Perm

def Sched_lpt(LM, LT, Mcoeff):
    return SchedJuxtapose(LM, LT, Mcoeff, algo = lpt.lpt)


def SchedJuxtapose(LM, LT, Mcoeff, algo = PTAS.PTAS):
    """Return the combination of M1 and M2 which costs the least"""

    LT1 = LTCutinTwo(LT)[0]
    LT2 = LTCutinTwo(LT)[1]

    Perm = PermutationGenerator(len(LM))

    CostC1list=[]
    CostC2list=[]
    CostEachMax=[]

    for i in range (len(LM)-1):
        LM1 = ds.create_LM(Perm[i][0])
        if Perm[i][0] == 1:
            LM1_done = lpt.lpt(LM1, LT1, Mcoeff)
        else: LM1_done = algo(LM1, LT1, Mcoeff, len(LT1)) #LM1_done is a list of list which contains all Type1 tasks optimally distributed(using algopart M1 of M
        CostC1 = 0 # Reinitialisation of CostC1
        CostC1 = lpt.final_cost_LM_1type(LM1_done) # we stock the cost of the machine which has the maximum cost
        CostC1list.append(CostC1) # We stock the CostC1 of each combination in CostC1List[]

    for j in range (len(LM)-1):
        LM2 = ds.create_LM(Perm[j][1])
        if Perm[j][1] == 1:
            LM2_done = lpt.lpt(LM2, LT2, Mcoeff)
        else: LM2_done = algo(LM2, LT2, Mcoeff, len(LT2)) # LM2_done is a list of list which contains all Type2 tasks optimally distributed(using LPT) to part M2 of M
        CostC2 = 0 # Reinitialisation of CostC2
        CostC2 = lpt.final_cost_LM_1type(LM2_done) # we stock the cost of the machine which has the maximum cost
        CostC2list.append(CostC2) # We stock the CostC2 of each combination in CostC2List[]

    # We aim to find the min(max(CostC1list[k],CostC2list[k])), then k-th element in Perm would be the most optimal combination
    # 1st step: we stock each max(CostC1list[k],CostC2list[k]) in CostEachMax[]
    for k in range (len(LM)-1):
        eachMax = max(CostC1list[k],CostC2list[k])
        CostEachMax.append(eachMax)

    # 2nd step: we find the indice that contains the minimal value in the list CostEachMax
    indiceMin = CostEachMax.index(min(CostEachMax))
    LM1f = ds.create_LM(Perm[indiceMin][0])
    if Perm[indiceMin][0] == 1:
        LM1f_done = lpt.lpt(LM1f, LT1, Mcoeff)
    else: LM1f_done = algo(LM1f, LT1, Mcoeff, 5)
    LM2f = ds.create_LM(Perm[indiceMin][1])
    if Perm[indiceMin][1] == 1:
        LM2f_done = lpt.lpt(LM2f, LT2, Mcoeff)
    LM2f_done = algo(LM2f, LT2, Mcoeff, 5)
    LM = LM1f_done + LM2f_done
    return LM






