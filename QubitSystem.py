#!/usr/bin/env python3

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib
import random
import sys

Hadamard_matrix = (1/math.sqrt(2))*np.array([(1,1), (1,-1)],dtype=np.float)
NOT_matrix = np.array([(0,1),(1,0)],dtype=np.float)
square_root_not_matrix = 0.5*np.array([(complex(1,1),complex(1,-1)),(complex(1,-1),complex(1,1))])
class QubitRegister:

    #init_state = initial state
    #n_qubits = number of qubits in the system
    def __init__(self,n_qubits, label='qs X'):
        self.n_qubits = n_qubits
        self.n_states= 2**n_qubits
        # print(f'0b{self.n_states:b}')
        #equals to write an 1 to the n qubit number
        # self.n_states_2 = 1 << n_qubits
        # print(f'0b{self.n_states_2}')

        self.label = label

        print("Quantum System Allocated")
        print(f"Number of qubits = {self.n_qubits}")
        print(f"Number of possible states = {self.n_states}")

        #allocate qubit system as an array of complex numbers

        self.states = np.zeros((self.n_states),dtype=np.complex) #It rapresent the 2^n hilbert state of the qubits in the register
        self.ampli_qubit = np.zeros((self.n_states),dtype=np.float)        
        self.phase_qubit = np.zeros((self.n_states),dtype=np.float)

        self.identity_matrix = np.array([(1,0), (0,1)])
    
    ### Implementaion of the various operations (gate)
    ### Every gate is square unitary matrices.
    
    def generic_Q_gate(self,t, *c, operation):
        """
        Implementation of the algorithm from the paper: https://arxiv.org/pdf/1601.07195.pdf (section2)
        For executiing single-qubit gate operations.
        
        Arguments:
        t (int): number of qubit in which you want apply the gate
        c (int): control qubits (they can be 0, 1 or multiple)
        operation: The gate you want to apply (It must by a 2x2 matrix).
        """
        
        #Check if the control qubit are valid
        
        #flattening the control qubits
        c=np.asarray(c)
        c= c.flatten()
        # print(f"C = {c}")
        for control_qubit in c:
            if control_qubit >= self.n_qubits:
                print("Invalid input. Control qubit not present in the system. Not executing.")
                sys.exit(0)
        #check if the input qubit is valid
        if t >= self.n_qubits:
            print("Invalid input. Qubit not present in the system. Not executing.")
            sys.exit(0)
        else:
            for g in range(0,self.n_states,2**(t+1)):
                # print(f"g:{g}")
                
                for i in range(g,(g+(2**t)),1):
                    
                    # For every control bit Check the c-th bit of the binary rapresentation of the states to check if it is one
                    a = i
                    b = i+2**t
                    exec = True
                    for control_qubit in c:
                        # print(f"ARR:{a:b},{a>>control_qubit}:{b:b},{b>>control_qubit} - c:{control_qubit}:{exec}")
                        if (a>>control_qubit)&1 and (b>>control_qubit)&1:
                            continue
                        else:
                            exec = False
                            break
                        

                    if exec: # if the control qubit array is empty (hence no control qubit is present) or if the control with the control qubit(s) is true
                        tmp=self.states[i]
                        self.states[i] = operation[0,0]*self.states[i]+operation[0,1]*self.states[i+(2**t)]
                        self.states[i+2**t] = operation[1,0]*tmp+operation[1,1]*self.states[i+(2**t)]

    def had(self,qubit_n):
        '''
        Apply the hadamard gate only to one qubit of the register.
        '''
        self.generic_Q_gate(qubit_n, operation=Hadamard_matrix)

    def NOT(self,qubit_n):
        '''
        Apply the NOT gate to one qubit of the register.
        '''
        self.generic_Q_gate(qubit_n, operation=NOT_matrix)

    def square_root_NOT(self,qubit_n):
        '''
        Apply the NOT gate to one qubit of the register.
        '''
        self.generic_Q_gate(qubit_n, operation=square_root_not_matrix)

    def P(self, qubit_n, angle):
        '''
        Corresponds to a rotation on the z-axis of the bloch sphere.
        In the circle notation, this rotation affect only the relative phase 
        of a qubit (hence it is normally seen just in the second sphere in a system with one qubit).
        It does not affect the amplitude.

        Arguments:
        angle (float): angle in radians.
        '''
        phase_matrix = np.array([(1,0),(0,math.e**(complex(0,angle)))])

        self.generic_Q_gate(qubit_n, operation=phase_matrix)
    
    def Z(self,qubit_n):
        '''
        Curiosity: the Z gate or P(Pi) or P(180degree) is equal to a series of gates -->[H]-->[NOT]-->[H]-- 
        '''
        self.P(qubit_n,math.pi)

    def S(self,qubit_n):
        self.P(qubit_n,math.pi/2)

    def T(self,qubit_n):
        self.P(qubit_n,math.pi/4)

    def ROTX(self, qubit_n, angle):
        '''
        Corresponds to a rotation on the x-axis of the bloch sphere.
        
        Arguments:
        angle (float): angle in radians.
        qubit_n: the number of the qubit you are applying the gate
        '''
        rotx_matrix = np.array([(math.cos(angle/2),-math.sin(complex(0,angle/2))),(-math.sin(complex(0,angle/2)),math.cos(angle/2))])

        self.generic_Q_gate(qubit_n, operation=rotx_matrix)
    
    def ROTY(self, qubit_n, angle):
        '''
        Corresponds to a rotation on the y-axis of the bloch sphere.
        
        Arguments:
        angle (float): angle in radians.
        qubit_n: the number of the qubit you are applying the gate
        '''
        roty_matrix = np.array([(math.cos(angle/2),-math.sin(angle/2)),(math.sin(angle/2)),math.cos(angle/2)])

        self.generic_Q_gate(qubit_n, operation=roty_matrix)

    ### CONTROLLED GATES ###

    def Chad(self, qubit_n, *control_qubits):
        '''
        Apply the hadamard gate only to one qubit of the register.
        '''
        self.generic_Q_gate(qubit_n, control_qubits, operation=Hadamard_matrix)

    def CNOT(self, qubit_n, *control_qubits):
        '''
        Apply the NOT gate to one qubit of the register.
        '''
        self.generic_Q_gate(qubit_n, control_qubits, operation=NOT_matrix)

    def Csquare_root_NOT(self, qubit_n, *control_qubits):
        '''
        Apply the NOT gate to one qubit of the register.
        '''
        self.generic_Q_gate(qubit_n, control_qubits, operation=square_root_not_matrix)

    def CP(self, qubit_n, *control_qubits, angle):
        '''
        Corresponds to a rotation on the z-axis of the bloch sphere.
        In the circle notation, this rotation affect only the relative phase 
        of a qubit (hence it is normally seen just in the second sphere in a system with one qubit).
        It does not affect the amplitude.

        Arguments:
        angle (float): angle in radians.
        '''
        phase_matrix = np.array([(1,0),(0,math.e**(complex(0,angle)))])

        self.generic_Q_gate(qubit_n, control_qubits, operation=phase_matrix)
    
    def CZ(self, qubit_n, *control_qubits):
        '''
        Curiosity: the Z gate or P(Pi) or P(180degree) is equal to a series of gates -->[H]-->[NOT]-->[H]-- 
        '''
        self.CP(qubit_n, control_qubits, angle=math.pi)

    def CS(self, qubit_n, *control_qubits):
        self.CP(qubit_n, control_qubits, angle=math.pi/2)

    def CT(self, qubit_n, *control_qubits):
        self.CP(qubit_n, control_qubits, angle=math.pi/4)

    def CROTX(self, qubit_n, *control_qubits, angle):
        '''
        Corresponds to a rotation on the x-axis of the bloch sphere.
        
        Arguments:
        angle (float): angle in radians.
        qubit_n: the number of the qubit you are applying the gate
        '''
        rotx_matrix = np.array([(math.cos(angle/2),-math.sin(complex(0,angle/2))),(-math.sin(complex(0,angle/2)),math.cos(angle/2))])

        self.generic_Q_gate(qubit_n, control_qubits, operation=rotx_matrix)
    
    def CROTY(self, qubit_n, *control_qubits, angle):
        '''
        Corresponds to a rotation on the y-axis of the bloch sphere.
        
        Arguments:
        angle (float): angle in radians.
        qubit_n: the number of the qubit you are applying the gate
        '''
        roty_matrix = np.array([(math.cos(angle/2),-math.sin(angle/2)),(math.sin(angle/2)),math.cos(angle/2)])

        self.generic_Q_gate(qubit_n, control_qubits, operation=roty_matrix)

    def SWAP(self, qubit_a, qubit_b):
        self.CNOT(qubit_a, qubit_b)
        self.CNOT(qubit_b, qubit_a)
        self.CNOT(qubit_a, qubit_b)
    
    def CSWAP(self, qubit_a, qubit_b, *control_qubits):
        
        self.CNOT(qubit_a, control_qubits+(qubit_b,))
        self.CNOT(qubit_b, control_qubits+(qubit_a,))
        self.CNOT(qubit_a, control_qubits+(qubit_b,))

    ### APPLYING GATE TO ALL THE QUBITS ###
    def NOT_transform(self):
        self.all_circuit = NOT_matrix
        for i in range(self.n_qubits-1):
            self.all_circuit = np.kron(NOT_matrix,self.all_circuit)
        self.states = self.all_circuit.dot(self.states)

    def had_transform(self):
        '''
        Apply the hadamard matrix only to all the qubits.
        '''
        self.all_circuit = Hadamard_matrix

        for i in range(self.n_qubits -1):
            self.all_circuit = np.kron(Hadamard_matrix,self.all_circuit)
        #apply hadamard matrix
        self.states = self.all_circuit.dot(self.states)
    
    def P_transform(self, angle):
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
        self.states = self.all_circuit.dot(self.states)
    
    def Z_transform(self):
        '''
        Curiosity: the Z gate or P(Pi) or P(180degree) is equal to a series of gates -->[H]-->[NOT]-->[H]-- 
        '''
        self.P_transform(math.pi)

    def S_transform(self):
        self.P_transform(math.pi/2)

    def T_transform(self):
        self.P_transform(math.pi/4)

    def ROTX_transform(self, angle):
        '''
        Corresponds to a rotation on the x-axis of the bloch sphere.
        
        Arguments:
        angle (float): angle in radians.
        '''
        self.rotx_matrix = np.array([(math.cos(angle/2),-math.sin(complex(0,angle/2))),(-math.sin(complex(0,angle/2)),math.cos(angle/2))])

        self.all_circuit = self.rotx_matrix
        for i in range(self.n_qubits-1):
            self.all_circuit = np.kron(self.rotx_matrix,self.all_circuit)
        self.states = self.all_circuit.dot(self.states)
    
    def ROTY_transform(self, angle):
        '''
        Corresponds to a rotation on the y-axis of the bloch sphere.
        
        Arguments:
        angle (float): angle in radians.
        '''
        self.roty_matrix = np.array([(math.cos(angle/2),-math.sin(angle/2)),(math.sin(angle/2)),math.cos(angle/2)])

        self.all_circuit = self.roty_matrix
        for i in range(self.n_qubits-1):
            self.all_circuit = np.kron(self.roty_matrix,self.all_circuit)
        self.states = self.all_circuit.dot(self.states)


    ###############################################################################

    ### More complex Operators implementation ####

    def increment(self):
        index = [i for i in range(self.n_qubits)]
        print(f"Index {index}")
        for i in range(self.n_qubits-1,-1,-1):
            print(f"Control qubits {index[:i]}, i: {i}")
            if(i==0):
                self.NOT(i)
            else:
                self.CNOT(i, index[:i])

    def decrement(self):
        index = [i for i in range(self.n_qubits)]
        print(f"Index {index}")
        for i in range(0,self.n_qubits):
            print(f"Control qubits {index[:i]}, i: {i}")
            if(i==0):
                self.NOT(i)
            else:
                self.CNOT(i, index[:i])

    def mirror(self):
        "Also known as Grover iteration"
        l=[i for i in range(self.n_qubits)]
        self.had_transform()
        self.NOT_transform()
        self.CZ(0, l[1:])
        self.NOT_transform()
        self.had_transform()

    def QFT(self):
        """
        Implementation of the Quantum Fourier Tranform (QFT) algorithm.
        """
        for i in reversed(range(self.n_qubits)):
            # print(f"QFT AAAAAA: {i}")
            self.had(i)
            n=1
            for j in reversed(range(i)):
                # print(f"QFT BBBBBB: {i},{j}")
                self.CP(i,j,angle=-math.pi/(2*n))
                n +=1
            # self.viz2()
        
        for i in range(math.floor(self.n_qubits/2)):
            # print(f"QFT: i: {i}, self.n_qubits-i: {self.n_qubits-1-i}")
            self.SWAP(i,self.n_qubits-1-i)
        # self.viz2()
    
    def IQFT(self):
        """
        Implementation of the Inverted QFT method
        """
        for i in range(math.floor(self.n_qubits/2),self.n_qubits):
            # print(f"QFT: i: {i}, self.n_qubits-i: {self.n_qubits-1-i}")
            self.SWAP(i,self.n_qubits-1-i)

        for i in range(self.n_qubits):
            # print(f"QFT AAAAAA: {i}")
            self.had(i)
            n=1
            for j in range(i):
                # print(f"QFT BBBBBB: {i},{j}")
                self.CP(i,j,angle=-math.pi/(2*n))
                n +=1
            # self.viz2()
        
        
        # self.viz2()
    
    ### Utils ###

    def get_NAA(self):
        """
        Return the Number of Amplitude Aplifications needed to maximize the 
        probability
        """
        return math.floor(math.pi*math.sqrt(self.n_states)/4)
    
    def get_NAA_multiple_markers(self,m):
        """
        Return the Number of Amplitude Aplifications needed to maximize the 
        probability
        """
        return math.floor((math.pi/4)*math.sqrt(self.n_states/m))

    # Read the state of the qubits, it "destroy" super position 
    def read(self):
        self.possible_outcome = np.arange(self.n_states)
        self.prob_qubit = np.square(np.absolute(self.states))
        #weighted random number generation
        x = random.choices(self.possible_outcome,weights=self.prob_qubit)
        print(f"Read Quantum State = {x}")

    #to make multiple mesurements and plot
    def read_multiple(self, n_shots=1000):
        self.possible_outcome = np.arange(self.n_states)
        self.prob_qubit = np.square(np.absolute(self.states))
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
        self.states[self.init_state]= 1.0
    
    def write_binary(self, binaryString):
        #convert to decimal
        self.init_state = int(binaryString, 2)
        print("Init state = ",self.init_state)
        if (self.init_state > self.n_states-1):
            print("Initial state can't represented in the system")
            sys.exit(1)
        #write the state to the qubit System
        self.states[self.init_state]= 1.0

    #circle notation representtation
    def viz2(self):
        # calculate amplitude and phase
        # calculate the amplitude and the phase of the states

        self.prob_qubit = np.absolute(self.states)
        print("Prob = ",self.prob_qubit)
        self.phase_qubit = np.angle(self.states)
        print("Phase = ",self.phase_qubit)
        #viz par
        rows = int(math.ceil(self.n_states /8.0))
        cols = min(self.n_states, 8)
        # print(type(rows),rows,type(cols),cols)
        fig, axs = plt.subplots(rows, cols,squeeze=False)
        # print(type(axs[0]),axs[0])
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













