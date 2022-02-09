import random as rn
import time
import numpy as np
import math
import matplotlib.pyplot as plt
import multiprocessing as mp

methods=['Random','Numpy','BadRandom','LCG']

l= int(len(methods))
DIS=[[]for i in range(l)]
CHI=[0 for i in range(l)]

runrange=1000

def LCG(min,max,seed):#A purposefully bad random number generator with an pretty good distribution but bad in a bitmap
    a = 7
    c = 31
    LCG = ((a*seed)+c) % max
    return int(LCG)

def bad_random(min,max,seed):#A purposefully bad random number generator with an pretty bad distribution but good in a bitmap
    c=round(max/2+((max+min)/2 * (math.cos(math.pi*math.cos(5000*seed**2)))))
    return int(c)

def CreateDistributionTimeLim(type,duration):#creates the distribution and puts it in an array. Ex. x is 4 and DIS[4] gets one added to it
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

def SumList(LIST):
    x=0
    for i in range(len(LIST)):
        x=x+LIST[i]
    return int(x)

def RelativeDistribution(DIS):
    MA=[0,0,0,0]
    for i in range(l):MA[i]=SumList(DIS[i])
    RA=[[]for i in range(l)]
    for i in range(l):
        X=[0 for i in range(runrange)]
        for j in range(runrange):X[j]= DIS[i][j]/MA[i]
        RA[i]=X
    return RA

def Plot(DIS,CHI):#does the ploting
    start=time.time()
    RA =RelativeDistribution(DIS)
    print("Computing RA took : "+str(time.time()-start)+"s")
    X=[[j for j in range(runrange)]for j in range(l)]
    for i in range(l):plt.plot(X[i], RA[i], label=methods[i])
    plt.ylim([0.8/runrange, 1.2/runrange])
    plt.title(str(runtime)+" seconds runtime")
    plt.legend(loc='upper right')
    plt.show()


def Output():#Prints to terminal
    MA=[0,0,0,0]
    for i in range(l):MA[i]=SumList(DIS[i])
    print()
    print("The amount of runs the different RNG achieved in "+str(runtime)+"s")
    print(methods)
    print(MA)
    print()

if __name__ == '__main__':
    with mp.Pool(processes=l) as pool:#starts a a process for every method
        runtime=float(input("runtime(in seconds) = "))
        multiple_results = [pool.apply_async(CreateDistributionTimeLim, (i,runtime,)) for i in range(4)]#starts async calculations
        DIS=[res.get() for res in multiple_results]#gets data
        pool.close#closes the pool
    Output()
    Plot(DIS,CHI)