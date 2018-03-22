import numpy as np
import mcfit
import matplotlib.pyplot as plt
import sys

Pk_location = 'Pk_CAMB_test.dat'

Pk_CAMB = np.loadtxt(Pk_location)

k_old = Pk_CAMB[:,0]
P_old = Pk_CAMB[:,1]

mu_values = [0.0]

k_min_values = [-4]
k_max_values = [3]
k_num_values = [5]

B1_values = np.linspace(1.5,1.5,num=1)
B2_values = np.linspace(0.1,0.1,num=1)
b1_values = np.linspace(0.1,0.2,num=5)
b2_values = np.linspace(3.64,3.64,num=1)

def get_C0(B1,B2):
    return 1 + (1/3)*(B1+B2) + (1/5)*B1*B2

def get_C2(B1,B2):
    return (2/3)*(B1+B2) + (4/7)*B1*B2

def get_C4(B1,B2):
    return (8/35)*B1*B2

xi_values = {}
r_values = {}

for mu in mu_values:

    P_mu_0 = np.polynomial.legendre.legval(mu,[1])
    P_mu_2 = np.polynomial.legendre.legval(mu,[0,0,1])
    P_mu_4 = np.polynomial.legendre.legval(mu,[0,0,0,0,1])

    for k_min in k_min_values:
        for k_max in k_max_values:
            for k_num in k_num_values:

                print('[{},{}], {}'.format(k_min,k_max,k_num))

                filename = 'xil/xil_{}_{}_{}.txt'.format(k_min,k_max,k_num)
                data = np.loadtxt(filename)

                r = data[:,0]
                xi0 = data[:,1]
                xi2 = data[:,2]
                xi4 = data[:,3]

                for B1 in B1_values:
                    for B2 in B2_values:
                        C0 = get_C0(B1,B2)
                        C2 = get_C2(B1,B2)
                        C4 = get_C4(B1,B2)
                        for b1 in b1_values:
                            for b2 in b2_values:

                                xi = (b1*b2)*(C0*xi0*P_mu_0 + C2*xi2*P_mu_2 + C4*xi4*P_mu_4)

                                new_xi_value = {(k_min,k_max,k_num): xi}
                                xi_values = {**xi_values,**new_xi_value}

                                new_r_value = {(k_min,k_max,k_num): r}
                                r_values = {**r_values,**new_r_value}

                                #plt.plot(r,xi*(r**2),label='[{},{}], {}'.format(k_min,k_max,k_num))
                                plt.plot(r,xi*(r**2),label='B1={}, B2={}, b1={}, b2={}'.format(B1,B2,b1,b2))
                                #plt.plot(r,xi*(r**2),label='mu={}'.format(mu))

plt.legend()
plt.xlim(0,200)
plt.show()
