#!/usr/bin/env python3

from sympy import Q
import QubitSystem as qs
import math

def bell_circuit():
    qsA = qs.QubitRegister(2, "bell_register")
    # qsA.write(3)
    qsA.write_binary('00')
    qsA.viz2()
    qsA.had(0)
    qsA.viz2()   
    qsA.CNOT(1,0)
    qsA.viz2()

if __name__ == '__main__':
    qsA = qs.QubitRegister(4, "register A")
    # qsA.write(3)
    qsA.write_binary('0000')
    # print(qsA.qubits)
    qsA.had_transform()
    qsA.NOT(2)
    qsA.NOT(3)
    qsA.CZ(0,1,2,3)
    qsA.NOT(2)
    qsA.NOT(3)
    # qsA.P(2,angle=math.pi/4)
    qsA.viz2()
    for i in range(qsA.get_NAA()):
        qsA.NOT(2)
        qsA.NOT(3)
        qsA.CZ(0,1,2,3)
        qsA.NOT(2)
        qsA.NOT(3)
        qsA.mirror()
        qsA.viz2()
    # qsA.increment()
    # qsA.had_transform()
    # # # qsA.P(math.pi/2)
    # # # qsA.had_transform()
    # qsA.viz2()
    # qsA.CP(0,2,math.pi/3)

    # # # qsA.had(1)
    # # # qsA.square_root_NOT()
    # # # qsA.square_root_NOT()
    # # # qsA.P(math.pi/2)
    # # # qsA.T()

    # # # qsA.NOT(0)
    # # qsA.Chad(1,0)
    # # qsA.viz2()
    # # # qsA.CNOT(1,0)
    # qsA.viz2()
    # # # qsA.read_multiple()
    # # bell_circuit()

