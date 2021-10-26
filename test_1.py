#!/usr/bin/env python3

from sympy import Q
import QubitSystem as qs
import math
if __name__ == '__main__':
    qsA = qs.QubitSystem(2, "register A")
    # qsA.write(1)
    qsA.write_binary('10')
    print(qsA.qubits)
    qsA.viz2()

    # qsA.had_transform()
    # qsA.P(math.pi/2)
    # qsA.had_transform()
    # qsA.viz2()
    # qsA.had(1)
    # qsA.square_root_NOT()
    # qsA.square_root_NOT()
    # qsA.P(math.pi/2)
    # qsA.T()

    qsA.NOT_one_bit(2)
    qsA.viz2()
    # qsA.read_multiple()
