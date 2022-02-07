import random as rn
import time
import numpy as np
import math
import matplotlib.pyplot as plt
import multiprocessing as mp

methods=['Random','Numpy','BadRandom','LCG']


#if __name__ == "__main__":
    #sampals=10**int(input("Number of Samples in 10**x:"))
    #runrange=int(input("Run Range:"))
sampals=10**6
runrange=1000

l= int(len(methods))
DIS=[[]for i in range(l)]
CHI=[0 for i in range(l)]

def LCG(min,max,seed):
    a = 7
    c = 31
    LCG = ((a*seed)+c) % runrange
    return int(LCG)

def bad_random(min,max,seed):
    c=round(max/2+((max+min)/2 * (math.cos(math.pi*math.cos(5000*seed**2)))))
    return int(c)

def CreateDistribution(type):
    DIS = [0 for i in range(runrange)]
    if type==0:
        start=time.time()
        for i in range(sampals):
            x = rn.randint(0, len(DIS)-1)
            DIS[x] = DIS[x]+1
        print(methods[type]+" took: "+str(round(time.time()-start))+" s")
        return DIS
    if type==1:
        start=time.time()
        for i in range(sampals):
            x = np.random.randint(0, len(DIS))
            DIS[x] = DIS[x]+1
        print(methods[type]+" took: "+str(round(time.time()-start))+" s")
        return DIS
    if type==2:
        start=time.time()
        for i in range(sampals):
            x = bad_random(0, len(DIS)-1,i)
            DIS[x] = DIS[x]+1
        print(methods[type]+" took: "+str(round(time.time()-start))+" s")
        return DIS
    if type==3:
        start=time.time()
        for i in range(sampals):
            x = LCG(0, len(DIS)-1,i)
            DIS[x] = DIS[x]+1
        print(methods[type]+" took: "+str(round(time.time()-start))+" s")
        return DIS

def ChiCalc(DIS):
    chi=0
    for i in range(runrange):
        x=(DIS[i]-(sampals/runrange))
        chi = (x**2)/(sampals/runrange)+chi
    chi= chi/runrange
    return float(chi)

def Output(DIS,CHI):
    print()
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
    for i in range(len(methods)):
        x=[j for j in range(runrange)]
        plt.plot(x, DIS[i], label=methods[i])
    plt.show()

if __name__ == '__main__':
    # start 4 worker processes
    with mp.Pool(processes=l) as pool:
        multiple_results = [pool.apply_async(CreateDistribution, (i,)) for i in range(4)]
        time.sleep(0.1)
        pool.join
        DIS=[res.get() for res in multiple_results]
        pool.close
    for i in range(len(methods)):
        CHI[i]=[ChiCalc(DIS[i])]
    Output(DIS,CHI)
    Plot(DIS,CHI)