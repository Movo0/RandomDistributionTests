import random as rn
import numpy as np
import math
import matplotlib.pyplot as plt
from time import process_time

methods=['Random','Numpy','BadRandom','LCG']

sampals=10**int(input("Number of Samples in 10**x:"))
runrange=int(input("Run Range:"))
programmStart=process_time()

#Absolut Amount
DIS = [0 for i in range(runrange)]

def LCG(min,max,seed):
    a = 7
    c = 31
    LCG = ((a*seed)+c) % max
    return int(LCG)

def bad_random(min,max,seed):
    c=round(max/2+((max+min)/2 * (math.cos(math.pi*math.cos(5000*seed**2)))))
    return int(c)

def CreateDistribution(type):
    DIS = [0 for i in range(runrange)]

    if type==0:
        for i in range(sampals):
            x = rn.randint(0, len(DIS)-1)
            DIS[x] = DIS[x]+1
        return DIS
    if type==1:
        for i in range(sampals):
            x = np.random.randint(0, len(DIS))
            DIS[x] = DIS[x]+1
        return DIS
    if type==2:
        for i in range(sampals):
            x = bad_random(0, len(DIS)-1,i)
            DIS[x] = DIS[x]+1
        return DIS
    if type==3:
        for i in range(sampals):
            x = LCG(0, runrange,i)
            DIS[x] = DIS[x]+1
        return DIS

def ChiCalc(DIS):
    chi=0
    for i in range(runrange):
        x=(DIS[i]-(sampals/runrange))
        chi = (x**2)/(sampals/runrange)+chi
    chi= chi/runrange
    return float(chi)

def Output(DIS,CHI):
    for i in range(0,len(methods)):
        print(methods[i]+" Distribution")
        print(DIS[i])
        print()
    for i in range(0,len(methods)):
        print(methods[i]+" Chi")
        print(CHI[i])
        print()
    print("Number of sampals: "+str(sampals))
    print("Range: "+str(runrange))

def Plot(DIS,CHI):
    plt.figure(figsize=(9, 2))

    plt.subplot(121)
    plt.bar(methods, CHI)
    plt.ylim([0, 4])

    plt.subplot(122)
    plt.ylim([0.8*sampals/runrange, 1.2*sampals/runrange])
    X=[j for j in range(runrange)]
    for i in range(len(methods)):plt.plot(X, DIS[i], label=methods[i])
    plt.legend()
    plt.show()

print("Finished preparation at "+str(process_time()-programmStart)+"s")
print("Start Computing")

DISCalcStart=process_time()
DIS=[CreateDistribution(i) for i in range(len(methods))]
print("DIS Calc Time "+str(process_time()-DISCalcStart)+"s")

CHICalcStart=process_time()
CHI=[ChiCalc(DIS[i]) for i in range(len(methods))]
print("CHI Calc Time "+str(process_time()-CHICalcStart)+"s")
print()

Output(DIS,CHI)
print("Time took :"+str(process_time()-programmStart)+"s")
Plot(DIS,CHI)
exit()