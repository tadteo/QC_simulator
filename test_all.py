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
        print("\n\n")
        self.qubit_system = qs.QubitRegister(3,"Control Phase")
        self.qubit_system.write_binary('000')
        self.qubit_system.had_transform()
        self.qubit_system.CP(0,2,angle=math.pi/3)
        # self.qubit_system.viz2()
    
    def test_control_phase(self):
        # Test feature one.
        print(f"\n\nTesting control phase of between bit 0 and 2 with angle {math.pi/3}")
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

    def test_CCNOT(self):
        print(f"\n\nTesting CCNOT applied at 0 and controlled qith 1 and 2")
        self.qubit_system.CNOT(0,1,2)
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
        self.assertAlmostEqual(self.qubit_system.phase_qubit[5],math.pi/3,f"The qubit phase should be {math.pi/3}.")
        self.assertAlmostEqual(self.qubit_system.phase_qubit[6],math.pi/3,f"The qubit phase should be {math.pi/3}.")
        self.assertEqual(self.qubit_system.phase_qubit[7],0,"The qubit phase should be 0.")
        
class TestSwapTest(unittest.TestCase):
    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        print("\n\n")
            
    def test_swap_test_1(self):
        print(f"\n\nTesting control swap with configuration '000'")
        qubit_system = qs.QubitRegister(3,"Control Phase")
        qubit_system.write_binary('000')
        # qubit_system.viz2()
        qubit_system.had(2)
        # qubit_system.viz2()
        qubit_system.CSWAP(0,1,2)
        # qubit_system.viz2()
        qubit_system.had(2)
        # qubit_system.viz2()
        qubit_system.NOT(2)
        # qubit_system.viz2()
        # Test feature one.
        qubit_system.prob_qubit = np.absolute(qubit_system.states)
        print("Prob = ",qubit_system.prob_qubit)
        qubit_system.phase_qubit = np.angle(qubit_system.states)
        print("Phase = ",qubit_system.phase_qubit)
        self.assertAlmostEqual(qubit_system.prob_qubit[0],0,msg="The qubit prob should be 0.")
        self.assertAlmostEqual(qubit_system.prob_qubit[1],0,msg="The qubit prob should be 0.")
        self.assertAlmostEqual(qubit_system.prob_qubit[2],0,msg="The qubit prob should be 0.")
        self.assertAlmostEqual(qubit_system.prob_qubit[3],0,msg="The qubit prob should be 0.")
        self.assertAlmostEqual(qubit_system.prob_qubit[4],1,msg="The qubit prob should be 1.")
        self.assertAlmostEqual(qubit_system.prob_qubit[5],0,msg="The qubit prob should be 0.")
        self.assertAlmostEqual(qubit_system.prob_qubit[6],0,msg="The qubit prob should be 0.")
        self.assertAlmostEqual(qubit_system.prob_qubit[7],0,msg="The qubit prob should be 0.")
    
    def test_swap_test_2(self):
        print(f"\n\nTesting control swap with configuration '010'")
        qubit_system = qs.QubitRegister(3,"Control Phase")
        qubit_system.write_binary('010')
        # qubit_system.viz2()
        qubit_system.had(2)
        # qubit_system.viz2()
        qubit_system.CSWAP(0,1,2)
        # qubit_system.viz2()
        qubit_system.had(2)
        # qubit_system.viz2()
        qubit_system.NOT(2)
        # qubit_system.viz2()
        # Test feature one.
        qubit_system.prob_qubit = np.absolute(qubit_system.states)
        print("Prob = ",qubit_system.prob_qubit)
        qubit_system.phase_qubit = np.angle(qubit_system.states)
        print("Phase = ",qubit_system.phase_qubit)
        self.assertAlmostEqual(qubit_system.prob_qubit[0],0,msg="The qubit prob should be 0.")
        self.assertAlmostEqual(qubit_system.prob_qubit[1],0.5,msg="The qubit prob should be 0.")
        self.assertAlmostEqual(qubit_system.prob_qubit[2],0.5,msg="The qubit prob should be 0.")
        self.assertAlmostEqual(qubit_system.prob_qubit[3],0,msg="The qubit prob should be 0.")
        self.assertAlmostEqual(qubit_system.prob_qubit[4],0,msg="The qubit prob should be 1.")
        self.assertAlmostEqual(qubit_system.prob_qubit[5],0.5,msg="The qubit prob should be 0.")
        self.assertAlmostEqual(qubit_system.prob_qubit[6],0.5,msg="The qubit prob should be 0.")
        self.assertAlmostEqual(qubit_system.prob_qubit[7],0,msg="The qubit prob should be 0.")

        self.assertAlmostEqual(qubit_system.phase_qubit[0],0,msg="The qubit phase should be 0.")
        self.assertAlmostEqual(qubit_system.phase_qubit[1],math.pi,msg="The qubit phase should be 0.")
        self.assertAlmostEqual(qubit_system.phase_qubit[2],0,msg="The qubit phase should be 0.")
        self.assertAlmostEqual(qubit_system.phase_qubit[3],0,msg="The qubit phase should be 0.")
        self.assertAlmostEqual(qubit_system.phase_qubit[4],0,msg="The qubit phase should be 1.")
        self.assertAlmostEqual(qubit_system.phase_qubit[5],0,msg="The qubit phase should be 0.")
        self.assertAlmostEqual(qubit_system.phase_qubit[6],0,msg="The qubit phase should be 0.")
        self.assertAlmostEqual(qubit_system.phase_qubit[7],0,msg="The qubit phase should be 0.")

class TestIncrementDecrement(unittest.TestCase):
    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        print("\n\n")
            
    def test_increment(self):
        print(f"\n\nTesting increment operation. Initial input '0001'")
        qubit_system = qs.QubitRegister(4,"Control Phase")
        qubit_system.write_binary('0001')
        # qubit_system.viz2()
        qubit_system.had(2)
        # qubit_system.viz2()
        qubit_system.P(2,angle=math.pi/4)
        # qubit_system.viz2()
        qubit_system.increment()
        # qubit_system.viz2()

        qubit_system.prob_qubit = np.absolute(qubit_system.states)
        print("Prob = ",qubit_system.prob_qubit)
        qubit_system.phase_qubit = np.angle(qubit_system.states)
        print("Phase = ",qubit_system.phase_qubit)
        for i in range(qubit_system.n_states):
            if(i == 2):
                self.assertAlmostEqual(qubit_system.prob_qubit[i],1/math.sqrt(2),msg=f"The {i}-qubit prob should be 0.7")
                self.assertAlmostEqual(qubit_system.phase_qubit[i],0,msg=f"The {i}-phase should be 0")
            if(i == 6):
                self.assertAlmostEqual(qubit_system.prob_qubit[i],1/math.sqrt(2),msg=f"The {i}-qubit prob should be 0.")
                self.assertAlmostEqual(qubit_system.phase_qubit[i],math.pi/4,msg=f"The phase should be {math.pi/4}")
        else:
            self.assertAlmostEqual(qubit_system.prob_qubit[i],0,msg=f"The {i}-qubit prob should be 0.")
        
    def test_decrement(self):
        print(f"\n\nTesting decrement operation. Initial input '0001'")
        qubit_system = qs.QubitRegister(4,"Control Phase")
        qubit_system.write_binary('0001')
        # qubit_system.viz2()
        qubit_system.had(2)
        # qubit_system.viz2()
        qubit_system.P(2,angle=math.pi/4)
        # qubit_system.viz2()
        qubit_system.decrement()
        # qubit_system.viz2()

        qubit_system.prob_qubit = np.absolute(qubit_system.states)
        print("Prob = ",qubit_system.prob_qubit)
        qubit_system.phase_qubit = np.angle(qubit_system.states)
        print("Phase = ",qubit_system.phase_qubit)
        for i in range(qubit_system.n_states):
            if(i == 0):
                self.assertAlmostEqual(qubit_system.prob_qubit[i],1/math.sqrt(2),msg=f"The {i}-qubit prob should be 0.7")
                self.assertAlmostEqual(qubit_system.phase_qubit[i],0,msg=f"The {i}-phase should be 0")
            if(i == 4):
                self.assertAlmostEqual(qubit_system.prob_qubit[i],1/math.sqrt(2),msg=f"The {i}-qubit prob should be 0.")
                self.assertAlmostEqual(qubit_system.phase_qubit[i],math.pi/4,msg=f"The phase should be {math.pi/4}")
        else:
            self.assertAlmostEqual(qubit_system.prob_qubit[i],0,msg=f"The {i}-qubit prob should be 0.")
        
if __name__ == '__main__':
    unittest.main()
