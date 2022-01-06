#!/usr/bin/env python3

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib
import random
import sys
import QubitSystem as qs

def gcd(a,b):
    """Returns the greatest common divisor of a an b"""

    while(b):
        m = a%b
        a=b
        b=m
    return a

def shor_logic(N,repeat_period, coprime=2):
    """Given the repeat period, find the factors"""
    ar2 = coprime**(repeat_period/2.0)
    factor1 = gcd(N,ar2-1)
    factor2 = gcd(N,ar2+1)
    return factor1, factor2

def shorQPU(N,precision_bits, coprime=2):
    quantum_register = qs.QubitRegister(2*precision_bits, "shore register")
    quantum_register.write(1)
    # quantum_register.viz2()
    
    #init
    for i in range(precision_bits,2*precision_bits,1):
        # print("i:",i)
        quantum_register.had(i)

    #iter 0
    for i in range(precision_bits-1,0,-1):
        # print("i:",i)
        quantum_register.CSWAP(i,i-1,precision_bits)
    
    #iter1
    for i in range(precision_bits-1,1,-1):
        # print("i:",i)
        quantum_register.CSWAP(i,i-2,precision_bits+1)

    # quantum_register.viz2()

    #qft
    quantum_register.QFT_partial_register(precision_bits,2*precision_bits)
    
    initial_value = quantum_register.read()
    # print("initial .value:",initial_value)
    # Reading just the last qubits (precision_bits)
    last_value = initial_value >> precision_bits
    print(f"qft initial value:  {initial_value} = {bin(initial_value)}, last_value: {last_value}, {bin(last_value)}")
    
    return last_value
    # quantum_register.viz2()

def estimate_num_spikes(spike,n_range):
    if spike < n_range/2:
        spike = n_range - spike
    best_error = 1.0
    e0 = 0
    e1 = 0
    e2 = 0 
    actual = spike /n_range
    candidates = []
    for denom in range(spike):
        numerator = round(denom*actual)
        estimated = numerator/denom
        error = abs(estimated-actual)
        e0 = e1
        e1 = e2
        e2 = error

        #look for a local minimum which beats our current best error
        if (e1 <= best_error and e1 < e0 and e1 < e2):
            repeat_period = denom-1
            candidates.append(denom-1)
            best_error= e1
    return candidates

def shor(N, precision_bits, coprime=2):
    repeat_period = shorQPU(N,precision_bits,coprime)
    
    # estimated = estimate_num_spikes(repeat_period, 2**precision_bits)
    # if not estimated:
    #     print("Got empty estimate, no solution found, retry")
    #     sys.exit(1)
    # print("estimated: ",estimated)
    # for e in estimated:
    #     factor1, factor2 = shor_logic(N,e,coprime)

    factor1, factor2 = shor_logic(N,repeat_period,coprime)

    return [factor1, factor2]

def main():
    N= 45
    precision_bits=6
    coprime =2
    
    results = shor(N,precision_bits, coprime)
    print(f"The factors of {N} are: {results}")

if __name__ == "__main__":
    main()
