import numpy as np
import matplotlib.pyplot as plt
import math
import random as rn
methods=['BadRandom','LCG','Numpy','Random']

runrange=int(input("Run Range:"))

def bad_random(min,max,seed):#A bad numbergenerator
    c=round(max/2+((max+min)/2 * (math.cos(math.pi*math.cos(5000*seed**2)))))
    return int(c)

def LCG(min,max,seed):
    a = 7
    c = 31
    LCG = ((a*seed)+c) % runrange
    return int(LCG)

def CreateArray(x,y,type):#Creating arrays out of the different numbergenerators
    if type==1:arr = [[bad_random(0,1000,i*j)/1000 for i in range(0,x)]for j in range(0,y)]
    if type==2:arr = [[LCG(0,1000,i*j)/1000 for i in range(0,x)]for j in range(0,y)]
    if type==3:arr = [[np.random.randint(0,1000)/1000 for i in range(0,x)]for j in range(0,y)]
    if type==4:arr = [[rn.randint(0,1000)/1000 for i in range(0,x)]for j in range(0,y)]

    return arr

for i in range(1,5):#creating the plots
    plt.subplot(220+i)#making the subplots
    rand_array=CreateArray(runrange,runrange,i)
    plt.imshow(rand_array) #show your array with the selected colour
    plt.title(methods[i-1])#puting the titles


plt.tight_layout()
plt.show() #show the image