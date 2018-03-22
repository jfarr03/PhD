import numpy as np
import mcfit
import matplotlib.pyplot as plt
import sys

Pk_location = '/Users/James/Downloads/Pk_CAMB_test.dat'

Pk_CAMB = np.loadtxt(Pk_location)

k_old = Pk_CAMB[:,0]
P_old = Pk_CAMB[:,1]

k_min = int(sys.argv[1])
k_max = int(sys.argv[2])
k_num = int(sys.argv[3])

k_new = np.logspace(k_min,k_max,num=10**k_num,endpoint=False)
P_new = np.interp(k_new,k_old,P_old)

#Need to generate very good quality ones of these and then just load them in
r, xi0 = mcfit.cosmology.P2xi(k_new,l=0)(P_new)
r, xi2 = mcfit.cosmology.P2xi(k_new,l=2)(P_new)
r, xi4 = mcfit.cosmology.P2xi(k_new,l=4)(P_new)

filename = 'xil_{}_{}_{}.txt'.format(k_min,k_max,k_num)
data = np.array(list(zip(r,xi0,xi2,xi4)))
np.savetxt(filename,data)

B1_values = np.linspace(1.1,1.1,num=1)
B2_values = np.linspace(0.1,0.1,num=1)
b1_values = np.linspace(0.84,0.84,num=1)
b2_values = np.linspace(3.64,3.64,num=1)

def get_C0(B1,B2):
    return 1 + (1/3)*(B1+B2) + (1/5)*B1*B2

def get_C2(B1,B2):
    return (2/3)*(B1+B2) + (4/7)*B1*B2

def get_C4(B1,B2):
    return (8/35)*B1*B2

for B1 in B1_values:
    for B2 in B2_values:
        C0 = get_C0(B1,B2)
        C2 = get_C2(B1,B2)
        C4 = get_C4(B1,B2)
        for b1 in b1_values:
            for b2 in b2_values:
                xi = (b1*b2)*(C0*xi0 + C2*xi2 + C4*xi4)
                plt.plot(r,xi*(r**2),label='B1={}, B2={}, b1={}, b2={}'.format(B1,B2,b1,b2))

#plt.legend()
plt.xlim(0,200)
plt.show()
