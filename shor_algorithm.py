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
        print("i:",i)
        quantum_register.had(i)

    #iter 0
    for i in range(precision_bits-1,0,-1):
        print("i:",i)
        quantum_register.CSWAP(i,i-1,precision_bits)
    
    #iter1
    for i in range(precision_bits-1,1,-1):
        print("i:",i)
        quantum_register.CSWAP(i,i-2,precision_bits+1)

    # quantum_register.viz2()

    #qft
    quantum_register.QFT_partial_register(precision_bits,2*precision_bits)
    quantum_register.viz2()

def shor(N, precision_bits, coprime=2):
    repeat_period = shorQPU(N,precision_bits,coprime)
    factor1, factor2 = shor_logic(N,repeat_period,coprime)

    return [factor1, factor2]

def main():
    N= 15
    precision_bits =4
    coprime =2
    
    results = shor(N,precision_bits, coprime)
    print(f"The factors of {N} are: {results}")

if __name__ == "__main__":
    main()
