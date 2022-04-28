#!/usr/bin/env python3

from sympy import Q
import QubitSystem as qs
import time
import matplotlib.pyplot as plt

def main():
    elapsed_time =[]
    n = [x for x in range(21)]
    print(n)
    for i in range(21):
        qsA = qs.QubitRegister(i, "register A")
        # count time of execution of set of instructions    
        start_time = time.time()
        qsA.QFT()
        end_time = time.time()
        print(i, end_time - start_time)
        elapsed_time.append(end_time-start_time)
    #plot the times of execution of the QFT algorithm
    plt.plot(n,elapsed_time, 'ro')
    plt.xlabel('number of qubits')
    plt.ylabel('time of execution')
    plt.show()

if __name__ == '__main__':
    main()
    
