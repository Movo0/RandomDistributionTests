import random as rn
import time
import numpy as np
import math

methods=['Random','Numpy','BadRandom','LCG']

l=int(len(methods))

DIS=[[]for i in range(l)]
CHI=[0 for i in range(l)]
def Calll():
    return int(len(methods))
def Callmethods():
    return methods


def LCG(min,max,seed): #A purposefully bad random number generator with an pretty good distribution but bad in a bitmap
    a = 7
    c = 31
    LCG = ((a*seed)+c) % max
    return int(LCG)

def bad_random(min,max,seed): #A purposefully bad random number generator with an pretty bad distribution but good in a bitmap
    c=round(max/2+((max+min)/2 * (math.cos(math.pi*math.cos(5000*seed**2)))))
    return int(c)

def CreateDistributionTimeLim(type,duration,runrange): #creates the distribution and puts it in an array. Ex. x is 4 and DIS[4] gets one added to it
    DIS = [0 for i in range(runrange)]
    i=0
    if type==0:
        start=time.time()
        while time.time()-start<duration:
            x = rn.randint(0, len(DIS)-1)
            DIS[x] = DIS[x]+1
    if type==1:
        start=time.time()
        while time.time()-start<duration:
            x = np.random.randint(0, len(DIS))
            DIS[x] = DIS[x]+1
    if type==2:
        start=time.time()
        while time.time()-start<duration:
            i=1+i
            x = bad_random(0, len(DIS)-1,i)
            DIS[x] = DIS[x]+1
    if type==3:
        start=time.time()
        while time.time()-start<duration:
            i=1+i
            x = LCG(0, len(DIS),i)
            DIS[x] = DIS[x]+1
    return DIS

def RelativeDistribution(DIS,runrange): #gives back the the relative distribution
    RA=[[]for i in range(l)]
    for i in range(l):
        X=[0 for i in range(runrange)]
        for j in range(runrange):X[j]= DIS[i][j]/SumList(DIS[i])
        RA[i]=X
    return RA

def ChiCalc(DIS,runrange,): #does the chi calculation
    chi=0
    for i in range(runrange):
        x=(DIS[i]-(SumList(DIS)/runrange))
        chi = (x**2)/(SumList(DIS)/runrange)+chi
    return float(chi)

def SumList(LIST): #summes the list
    x=0
    for i in range(len(LIST)):
        x=x+LIST[i]
    return int(x)

def CalcV(CHI,DIS):
    CrV=[0 for i in range(l)]
    for i in range(l):CrV[i]=math.sqrt(CHI[i]/SumList(DIS[i]))  #calculates the  Cramér's V
    return CrV