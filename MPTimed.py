import time
import math
import matplotlib.pyplot as plt
import multiprocessing as mp
import RandomDistributionLib as RDL

l=RDL.Calll()
methods=RDL.Callmethods()

DIS=[[]for i in range(l)]
CHI=[0 for i in range(l)]

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



def Plot(RA): #does the ploting
    plt.figure("CHI Square Test Timed",figsize=(14, 10))

    plt.subplot(221) #Subplots the runamounts of each method
    plt.bar(methods, RA)
    plt.title("Amount of runs in "+str(runtime)+" seconds by different RNG")

    plt.subplot(222) #Subplots the Relative distribution
    RA =RDL.RelativeDistribution(DIS,runrange)
    X=[[j for j in range(runrange)]for j in range(l)]
    for i in range(l):plt.plot(X[i], RA[i], label=methods[i])
    plt.ylim([0.7/runrange, 1.3/runrange])
    plt.legend(loc='upper right')
    plt.title("The result off "+str(runtime)+" seconds runtime")

    plt.subplot(223) #Subplots the Chi's
    plt.bar(methods, CHI)
    plt.ylim([0, CHI[0]+CHI[1]])
    plt.title("Chi^2 of the different methods")

    plt.subplot(224) #Subplots the Cramér's V
    plt.bar(methods, CrV)
    plt.title("Cramér's V  (higher is worse)")

    plt.tight_layout()
    plt.savefig("MP.png")
    plt.show()



def Output(): #Prints to terminal
    print()
    for i in range(l):
        print()
        print("The amount of runs the different RNG achieved in "+str(runtime)+"s by "+methods[i])
        print(RA[i])
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
        multiple_results = [pool.apply_async(RDL.CreateDistributionTimeLim, (i,runtime,runrange,)) for i in range(l)] #starts async calculations
        pool.apply_async(TimeLeft(runtime,))
        DIS=[res.get() for res in multiple_results] #gets data and stores the values in DIS
        pool.close #closes the pool

    for i in range(len(methods)):CHI[i]=RDL.ChiCalc(DIS[i],runrange) #does the chi calculation

    RA=[0 for i in range(l)]
    for i in range(l):RA[i]=RDL.SumList(DIS[i]) #calculates the runamount in of runs in each method

    CrV=RDL.CalcV(CHI,DIS) #calculates the  Cramér's V
    
    Output()
    Plot(RA)
