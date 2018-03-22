import numpy as np
import mcfit
import matplotlib.pyplot as plt
import sys

Pk_location = 'Pk_CAMB_test.dat'

Pk_CAMB = np.loadtxt(Pk_location)

k_old = Pk_CAMB[:,0]
P_old = Pk_CAMB[:,1]

#k_min = int(sys.argv[1])
#k_max = int(sys.argv[2])
#k_num = int(sys.argv[3])

k_min_values = [-3,-4]
k_max_values = [2,3]
k_num_values = [3,4,5,6,7]

for k_min in k_min_values:
    for k_max in k_max_values:
        for k_num in k_num_values:
            print('working on k_min={}, k_max={}, k_num={}'.format(k_min,k_max,k_num))

            k_new = np.logspace(k_min,k_max,num=10**k_num,endpoint=False)
            P_new = np.interp(k_new,k_old,P_old)

            r, xi0 = mcfit.cosmology.P2xi(k_new,l=0)(P_new)
            r, xi2 = mcfit.cosmology.P2xi(k_new,l=2)(P_new)
            r, xi4 = mcfit.cosmology.P2xi(k_new,l=4)(P_new)

            filename = 'xil/xil_{}_{}_{}.txt'.format(k_min,k_max,k_num)
            data = np.array(list(zip(r,xi0,xi2,xi4)))
            np.savetxt(filename,data)
