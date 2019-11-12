import matplotlib.pyplot as plt
import numpy as np 
import math

while True:
    Npixeles = int(100*.8)
    t = int(input("Ingrasa un num entre 0 y "+str(Npixeles)+" : "))
    n = -5+10*(t/Npixeles)
    t2 = 1/(1+ math.exp(n))
    x = np.linspace(-5,5)
    y = []
    for i in x:
        y.append( 1/(1+ math.exp(i)))
    plt.plot(x,y)
    plt.plot(n,t2,"*r")
    plt.show()
