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
samples=500
runrange=10

l= int(len(methods))
DIS=[[]for i in range(l)]
CHI=[0 for i in range(l)]

def LCG(min,max,seed):#A purposefully bad random number generator with an pretty good distribution but bad in a bitmap
    a = 7
    c = 31
    LCG = ((a*seed)+c) % runrange
    return int(LCG)

def bad_random(min,max,seed):#A purposefully bad random number generator with an pretty bad distribution but good in a bitmap
    c=round(max/2+((max+min)/2 * (math.cos(math.pi*math.cos(5000*seed**2)))))
    return int(c)

def CreateDistribution(type):#creates the distribution and puts it in an array. Ex. x is 4 and DIS[4] gets one added to it
    DIS = [0 for i in range(runrange)]
    if type==0:
        start=time.time()
        for i in range(samples):
            x = rn.randint(0, len(DIS)-1)
            DIS[x] = DIS[x]+1
    if type==1:
        start=time.time()
        for i in range(samples):
            x = np.random.randint(0, len(DIS))
            DIS[x] = DIS[x]+1
    if type==2:
        start=time.time()
        for i in range(samples):
            x = bad_random(0, len(DIS)-1,i)
            DIS[x] = DIS[x]+1
    if type==3:
        start=time.time()
        for i in range(samples):
            x = LCG(0, len(DIS)-1,i)
            DIS[x] = DIS[x]+1
    print(methods[type]+" took: "+str(round(time.time()-start))+" s")
    return DIS

def ChiCalc(DIS):#does the chi calculation
    chi=0
    for i in range(runrange):
        x=(DIS[i]-(samples/runrange))
        chi = (x**2)/(samples/runrange)+chi
    return float(chi)

def Output():#does the terminal output
    print()
    Answer=input("Print Distribution? : ")
    if Answer=="Y"or Answer=="y"or Answer=="yes"or Answer=="Yes":
        for i in range(0,len(methods)):
            print(methods[i]+" Distribution")
            print(DIS[i])
            print()
    print()
    for i in range(0,len(methods)):
        print(methods[i]+" Chi")
        print(CHI[i])
        print()
    print("Number of samples: "+str(samples))
    print("Range: "+str(runrange))

def Plot():#does the ploting
    plt.figure(figsize=(18, 6))
    plt.title(str(samples)+" * "+str(runrange))
    plt.subplot(121)
    plt.bar(methods, CHI)
    plt.ylim([0, CHI[0]+CHI[1] ])

    plt.subplot(122)
    plt.ylim([0.8*samples/runrange, 1.2*samples/runrange])
    X=[j for j in range(runrange)]
    for i in range(len(methods)):plt.plot(X, DIS[i], label=methods[i])
    plt.legend(loc='upper right')
    plt.savefig("MPMain.png")
    plt.show()

if __name__ == '__main__':
    with mp.Pool(processes=l) as pool:#starts a a process for every method
        multiple_results = [pool.apply_async(CreateDistribution, (i,)) for i in range(4)]#starts async calculations
        DIS=[res.get() for res in multiple_results]#gets data
        pool.close#closes the pool
    for i in range(len(methods)):CHI[i]=ChiCalc(DIS[i])#does the chi calculation

    Output()
    Plot()