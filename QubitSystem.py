#!/usr/bin/env python3

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib
import random
import sys

class QubitSystem:

    #init_state = initial state
    #n_qubits = number of qubits in the system
    def __init__(self,n_qubits, label='qs X'):
        self.n_qubits = n_qubits
        self.n_states= 2**n_qubits
        self.label = label

        print("Quantum System Allocated")
        print(f"Number of qubits = {self.n_qubits}")
        print(f"Number of possible states = {self.n_states}")

        #allocate qubit system as an array of complex numbers

        self.qubits = np.zeros((self.n_states),dtype=np.complex)
        self.ampli_qubit = np.zeros((self.n_states),dtype=np.float)        
        self.phase_qubit = np.zeros((self.n_states),dtype=np.float)

        self.identity_matrix = np.array([(1,0), (0,1)])
    ### Implementaion of the various operations (gate)
    ### Every gate is square unitary matrices.
    def had_transform(self):
        '''
        Apply the hadamard matrix only to all the qubits.
        '''
        self.Hadamard_matrix = (1/math.sqrt(2))*np.array([(1,1), (1,-1)],dtype=np.float)
        self.all_circuit = self.Hadamard_matrix

        for i in range(self.n_qubits -1):
            self.all_circuit = np.kron(self.Hadamard_matrix,self.all_circuit)
        #apply hadamard matrix
        self.qubits = self.all_circuit.dot(self.qubits)

    def had(self,qubit):
        '''
        Apply the hadamard matrix only to one qubit.
        '''
        if qubit >= self.n_qubits:
            print("Invalid input. Qubit not present in the system.")
        self.Hadamard_matrix = (1/math.sqrt(2))*np.array([(1,1), (1,-1)],dtype=np.float)
        self.all_circuit = self.Hadamard_matrix #self.qubits

        for i in range(self.n_qubits -1):
            if i == qubit:
                self.all_circuit = np.kron(self.identity_matrix,self.all_circuit)
            else:
                self.all_circuit = np.kron(self.Hadamard_matrix,self.all_circuit)

        #apply hadamard matrix
        self.qubits = self.all_circuit.dot(self.qubits)
    
    def NOT(self):
        self.not_matrix = np.array([(0,1),(1,0)],dtype=np.float)
        self.all_circuit = self.not_matrix
        for i in range(self.n_qubits-1):
            self.all_circuit = np.kron(self.not_matrix,self.all_circuit)
        self.qubits = self.all_circuit.dot(self.qubits)
    
    def square_root_NOT(self):
        self.square_root_not_matrix = 0.5*np.array([(complex(1,1),complex(1,-1)),(complex(1,-1),complex(1,1))])
        self.all_circuit = self.square_root_not_matrix
        for i in range(self.n_qubits-1):
            self.all_circuit = np.kron(self.square_root_not_matrix,self.all_circuit)
        self.qubits = self.all_circuit.dot(self.qubits)

    def NOT_one_bit(self,qubit): #TODO: check this function for multiples qubits
        self.not_matrix = np.array([(0,1),(1,0)],dtype=np.float)
        self.identity_matrix = np.array([(1,0),(0,1)],dtype=np.float)
        if (qubit == 0):
            self.all_circuit = self.not_matrix
            for i in range(self.n_qubits-1):
                self.all_circuit = np.kron(self.identity_matrix,self.all_circuit)
        else:
            self.all_circuit = self.identity_matrix
            for i in range(qubit-1):
                self.all_circuit = np.kron(self.identity_matrix,self.all_circuit)
            self.all_circuit = self.all_circuit = np.kron(self.not_matrix,self.all_circuit)
            for i in range(qubit,self.n_qubits-1):
                self.all_circuit = np.kron(self.identity_matrix,self.all_circuit)
            
        self.qubits = self.all_circuit.dot(self.qubits)

    def P(self, angle):
        '''
        Corresponds to a rotation on the z-axis of the bloch sphere.
        In the circle notation, this rotation affect only the relative phase 
        of a qubit (hence it is normally seen just in the second sphere in a system with one qubit).
        It does not affect the amplitude.


        Arguments:
        angle (float): angle in radians.
        '''
        self.phase_matrix = np.array([(1,0),(0,math.e**(complex(0,angle)))])

        self.all_circuit = self.phase_matrix
        for i in range(self.n_qubits-1):
            self.all_circuit = np.kron(self.phase_matrix,self.all_circuit)
        self.qubits = self.all_circuit.dot(self.qubits)
    
    def Z(self):
        '''
        Curiosity: the Z gate or P(Pi) or P(180degree) is equal to a series of gates -->[H]-->[NOT]-->[H]-- 
        '''
        self.P(math.pi)

    def S(self):
        self.P(math.pi/2)

    def T(self):
        self.P(math.pi/4)

    def ROTX(self, angle):
        '''
        Corresponds to a rotation on the x-axis of the bloch sphere.
        
        Arguments:
        angle (float): angle in radians.
        '''
        self.rotx_matrix = np.array([(math.cos(angle/2),-math.sin(complex(0,angle/2))),(-math.sin(complex(0,angle/2)),math.cos(angle/2))])

        self.all_circuit = self.rotx_matrix
        for i in range(self.n_qubits-1):
            self.all_circuit = np.kron(self.rotx_matrix,self.all_circuit)
        self.qubits = self.all_circuit.dot(self.qubits)

    def ROTY(self, angle):
        '''
        Corresponds to a rotation on the y-axis of the bloch sphere.
        
        Arguments:
        angle (float): angle in radians.
        '''
        self.roty_matrix = np.array([(math.cos(angle/2),-math.sin(angle/2)),(math.sin(angle/2)),math.cos(angle/2)])

        self.all_circuit = self.roty_matrix
        for i in range(self.n_qubits-1):
            self.all_circuit = np.kron(self.roty_matrix,self.all_circuit)
        self.qubits = self.all_circuit.dot(self.qubits)


    # Read the state of the qubits, it "destroy" super position 
    def read(self):
        self.possible_outcome = np.arange(self.n_states)
        self.prob_qubit = np.square(np.absolute(self.qubits))
        #weighted random number generation
        x = random.choices(self.possible_outcome,weights=self.prob_qubit)
        print(f"Read Quantum State = {x}")

    #to make multiple mesurements and plot
    def read_multiple(self, n_shots=1000):
        self.possible_outcome = np.arange(self.n_states)
        self.prob_qubit = np.square(np.absolute(self.qubits))
        #initialize vector for measurements
        self.measurements_state = np.zeros((self.n_states),dtype=np.int)
        #mesure n_shot times
        for i in range(n_shots):
            x = random.choices(self.possible_outcome,weights=self.prob_qubit)
            self.measurements_state[x]=self.measurements_state[x] +1
        plt.grid(b=True)
        plt.bar(self.possible_outcome,self.measurements_state/n_shots)
        plt.xlabel("Quantum states")
        plt.ylabel("Probability")
        plt.xticks(self.possible_outcome, rotation = '65')
        plt.show()
    
    #write value to the qubit system
    def write(self,init_state):
        self.init_state = init_state
        print("Written state = ",self.init_state)
        # check that the initial state is correct 
        if (self.init_state > self.n_states-1):
            print("Initial state can't represented in the system")
            sys.exit(1)
        #write the state to the qubit system
        self.qubits[self.init_state]= 1.0
    
    def write_binary(self, binaryString):
        #convert to decimal
        self.init_state = int(binaryString, 2)
        print("Init state = ",self.init_state)
        if (self.init_state > self.n_states-1):
            print("Initial state can't represented in the system")
            sys.exit(1)
        #write the state to the qubit System
        self.qubits[self.init_state]= 1.0

    #circle notation representtation
    def viz2(self):
        # calculate amplitude and phase
        # calculate the amplitude and the phase of the states

        self.prob_qubit = np.absolute(self.qubits)
        print("Prob = ",self.prob_qubit)
        self.phase_qubit = np.angle(self.qubits)
        print("Phase = ",self.prob_qubit)
        #viz par
        rows = int(math.ceil(self.n_states /8.0))
        cols = min(self.n_states, 8)
        print(type(rows),rows,type(cols),cols)
        fig, axs = plt.subplots(rows, cols,squeeze=False)
        print(type(axs[0]),axs[0])
        for row in range(rows):
            for col in range(cols):
                #amplitude area
                circleExt = matplotlib.patches.Circle((0.5,0.5), 0.5, color='gray',alpha=0.25)
                circleInt = matplotlib.patches.Circle((0.5,0.5), self.prob_qubit[(row*8)+col]/2, color='b', alpha=0.3)
                axs[row][col].add_patch(circleExt)
                axs[row][col].add_patch(circleInt)
                axs[row][col].set_aspect('equal')
                state_number = "|" + str((row*8)+col) + ">"
                axs[row][col].set_title(state_number)
                x1 = [0.5, 0.5 + 0.5*self.prob_qubit[(row*8)+col]*math.cos(self.phase_qubit[(row*8)+col] + np.pi/2)]
                y1 = [0.5, 0.5 + 0.5*self.prob_qubit[(row*8)+col]*math.sin(self.phase_qubit[(row*8)+col] + np.pi/2)]

                axs[row][col].plot(x1,y1,'r')
                axs[row][col].axis('off')
        
        plt.show()













