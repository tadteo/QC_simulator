#!/usr/bin/env python3

from sympy import Q
import QubitSystem as qs
import math
import numpy as np
import unittest
from test import support

class TestBellCircuit(unittest.TestCase):
    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        print("Testing the bell circuit")
        self.qubit_system = qs.QubitRegister(2,"bell_register")
        self.qubit_system.write_binary('00')
        self.qubit_system.had(0)
        self.qubit_system.CNOT(1,0)
        # self.qubit_system.viz2()
    
    def test_bell_circuit(self):
        # Test feature one.
        self.qubit_system.prob_qubit = np.absolute(self.qubit_system.states)
        print("Prob = ",self.qubit_system.prob_qubit)
        self.qubit_system.phase_qubit = np.angle(self.qubit_system.states)
        print("Phase = ",self.qubit_system.phase_qubit)
        self.assertGreater(self.qubit_system.prob_qubit[0],0.5,"The result should be a superposition of ∣0⟩ and ∣3⟩.")
        self.assertEqual(self.qubit_system.prob_qubit[1],0,"The result should be a superposition of ∣0⟩ and ∣3⟩.")
        self.assertEqual(self.qubit_system.prob_qubit[2],0,"The result should be a superposition of ∣0⟩ and ∣3⟩.")
        self.assertGreater(self.qubit_system.prob_qubit[3],0.5,"The result should be a superposition of ∣0⟩ and ∣3⟩.")

class TestControlPhase(unittest.TestCase):
    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        print(f"\n\nTesting control phase of between bit 0 and 2 with angle {math.pi/3}")
        self.qubit_system = qs.QubitRegister(3,"Control Phase")
        self.qubit_system.write_binary('000')
        self.qubit_system.had_transform()
        self.qubit_system.CP(0,2,math.pi/3)
        # self.qubit_system.viz2()
    
    def test_control_phase(self):
        # Test feature one.
        self.qubit_system.prob_qubit = np.absolute(self.qubit_system.states)
        print("Prob = ",self.qubit_system.prob_qubit)
        self.qubit_system.phase_qubit = np.angle(self.qubit_system.states)
        print("Phase = ",self.qubit_system.phase_qubit)
        self.assertEqual(self.qubit_system.phase_qubit[0],0,"The qubit phase should be 0.")
        self.assertEqual(self.qubit_system.phase_qubit[1],0,"The qubit phase should be 0.")
        self.assertEqual(self.qubit_system.phase_qubit[2],0,"The qubit phase should be 0.")
        self.assertEqual(self.qubit_system.phase_qubit[3],0,"The qubit phase should be 0.")
        self.assertEqual(self.qubit_system.phase_qubit[4],0,"The qubit phase should be 0.")
        self.assertEqual(self.qubit_system.phase_qubit[5],math.pi/3,f"The qubit phase should be {math.pi/3}.")
        self.assertEqual(self.qubit_system.phase_qubit[6],0,"The qubit phase should be 0.")
        self.assertEqual(self.qubit_system.phase_qubit[7],math.pi/3,f"The qubit phase should be {math.pi/3}.")


if __name__ == '__main__':
    unittest.main()

    for i in range(8):
        qsA = qs.QubitRegister(i, "register A")
        for j in range(i):
            qsA.write(i)
            # qsA.write_binary('0')
            print(qsA.states)
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

            # qsA.NOT_one_bit(2)
            # qsA.NOT(0)
            qsA.had(1)
            qsA.viz2()
            # qsA.read_multiple()
