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

def ChiCalc(DIS): #does the chi calculation
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

def RelativeDistribution(DIS): #gives back the the relative distribution
    RA=[[]for i in range(l)]
    for i in range(l):
        X=[0 for i in range(runrange)]
        for j in range(runrange):X[j]= DIS[i][j]/MA[i]
        RA[i]=X
    return RA

def TimeLeft(duration): #tracks the time and prints it to make sure the code is still running
    start=time.time()
    updateTime=1
    z=0
    while time.time()-start<duration:
        time.sleep(updateTime)
        z=z+1
        print("Time elapsed "+str(updateTime*z)+"s   "+str(round(updateTime*z*100/duration))+"%  done", end="\r")
    print("Time elapsed "+str(duration)+"s   100%  done", end="\r")
    return



def Plot(): #does the ploting
    Answer=input("Also show Plots seperat: ")

    plt.figure("CHI Square Test Timed",figsize=(18, 6))

    plt.subplot(141) #Subplots the runamounts of each method
    plt.bar(methods, MA)
    plt.title("Amount of runs in "+str(runtime)+" seconds by different RNG")

    plt.subplot(142) #Subplots the Relative distribution
    RA =RelativeDistribution(DIS)
    X=[[j for j in range(runrange)]for j in range(l)]
    for i in range(l):plt.plot(X[i], RA[i], label=methods[i])
    plt.ylim([0.7/runrange, 1.3/runrange])
    plt.legend(loc='upper right')
    plt.title("The result off "+str(runtime)+" seconds runtime")

    plt.subplot(143) #Subplots the Chi's
    plt.bar(methods, CHI)
    plt.ylim([0, CHI[0]+CHI[1]])
    plt.title("Chi^2 of the different methods")

    plt.subplot(144) #Subplots the Cramér's V
    plt.bar(methods, CrV)
    plt.title("Cramér's V  (higher is worse)")

    plt.tight_layout()
    plt.show()
    if Answer=="Y"or Answer=="y"or Answer=="yes"or Answer=="Yes": # the same just seperat
        plt.figure("Runs per Method")
        plt.bar(methods, MA)
        plt.title("Amount of runs in "+str(runtime)+" seconds by different RNG")
        plt.show()

        plt.figure("Relative distribution")
        RA =RelativeDistribution(DIS)
        X=[[j for j in range(runrange)]for j in range(l)]
        for i in range(l):plt.plot(X[i], RA[i], label=methods[i])
        plt.ylim([0.7/runrange, 1.3/runrange])
        plt.legend(loc='upper right')
        plt.title("The result off "+str(runtime)+" seconds runtime")
        plt.show()

        plt.figure("Chi")
        plt.bar(methods, CHI)
        plt.ylim([0, CHI[1]+CHI[2]])
        plt.title("Chi^2 of the different methods")
        plt.show()

        plt.figure("Cramér's V")
        plt.bar(methods, CrV)
        plt.title("Cramér's V  (higher is worse)")
        plt.show()



def Output(): #Prints to terminal
    print()
    for i in range(l):
        print()
        print("The amount of runs the different RNG achieved in "+str(runtime)+"s by "+methods[i])
        print(MA[i])
        print()
        print(methods[i]+" Chi2")
        print(CHI[i])
        print("Cramér's V is")
        print(CrV[i])
        print()
    print("Lower Cramér's V is better")

if __name__ == '__main__': #Actual calculation start
    with mp.Pool(processes=l+1) as pool: #starts a a process for every method
        runtime=float(input("Runtime(in seconds) = "))
        runrange=int(input("Runrange = "))
        multiple_results = [pool.apply_async(CreateDistributionTimeLim, (i,runtime,runrange,)) for i in range(l)] #starts async calculations
        pool.apply_async(TimeLeft(runtime,))
        DIS=[res.get() for res in multiple_results] #gets data and stores the values in DIS
        pool.close #closes the pool

    for i in range(len(methods)):CHI[i]=ChiCalc(DIS[i]) #does the chi calculation

    MA=[0 for i in range(l)]
    for i in range(l):MA[i]=SumList(DIS[i]) #calculates the runamount in of runs in each method

    CrV=[0 for i in range(l)]
    for i in range(l):CrV[i]=math.sqrt(CHI[i]/MA[i])  #calculates the  Cramér's V

    Output()
    Plot()
