import numpy as np
from random import randint

# Agent class with scalar value consensus
class Agents:
    def __init__(self,id, F):
        self.id = id
        self.xi= randint(-1000,1000)
        self.qi = 0
        self.collected_qs = 0
        self.activation_history = []
        self.F = F
        self.Q_i = []
        self.history =[self.xi]
        self.connections = []
    
    # Add agents as its neighbors
    def connect(self, agents):
        for aa in agents:
            self.connections.append(aa)

    # Returns its neighbor set
    def neighbors(self):
        return self.connections
    
    # Reset its neighbor set
    def neighbor_rest(self):
        self.connections = []

    # Send its values to its neighbors
    # If the type is 1, that means the value is a state xi. Otherwise, it is activation status qi
    # Only share if qi is 1
    def propagate(self, type_check=1):
        value = self.xi if type_check else self.qi
        if self.qi:
            for neigh in self.neighbors():
                neigh.receive(value, type_check)

    # Receive values from its neighbors
    # If the type is 1, that means the value is a state xi. Otherwise, it is activation status qi
    def receive(self, value, type_check):
        if type_check:
            self.Q_i.append(value)
        else:
            self.collected_qs+=value

    # BP: they share qi with their out-neighbors, and if they have received qi=1 from at least r in-neighbors, they set qi to 1
    def bp(self,r):          
        self.activation_history.append(self.qi)
        self.propagate(0)
        if self.collected_qs >= r:
            self.qi = 1
        else:
            self.qi = 0
        self.collected_qs = 0


    # Performs W-MSR
    # Divide the values into three lists
    # O_i: values smaller than self.xi
    # H_i: values bigger than self.xi
    # comb_list: values equal to self.xi
    def w_msr(self):
    
        O_i =[v for v in self.Q_i if v < self.xi]
        comb_list = [v for v in self.Q_i if v == self.xi] + [self.xi]
        H_i = [v for v in self.Q_i if v > self.xi]

        # Remove the F smallest values from O_i
        O_i = sorted(O_i)
        O_i = O_i[self.F:]

        # Remove the F largest values from H_i
        H_i = sorted(H_i)
        if self.F > 0:
            H_i = H_i[:-self.F]

        # Weighted averge of the remaining values
        Q_i_not_R_i = O_i+ comb_list + H_i
        self.xi =  sum(Q_i_not_R_i)/len(Q_i_not_R_i)

        self.history.append(self.xi)
        self.Q_i = []


    # Performs SW-MSR. It takes an additional parameter T. 
    # It collects states for T time steps and updates its own state every T steps
    def sw_msr(self, t, T):
        if (t+1) % T == 0 or t<T:
            self.w_msr()
        else:
            self.history.append(self.xi)


    # Performs BP-MSR: run W-MSR only if qi is 1
    def bp_msr(self):
        if not self.qi:
            self.Q_i = []
            self.history.append(self.xi)
            return
        self.w_msr()


# Normal leader class
class Leaders(Agents):
    def __init__(self,id, value, F):
        super().__init__(id, F)
        self.xi = value
        self.qi = 1
        self.history =[self.xi]
    
    # Receive values from its neighbors: don't do anything
    def receive(self, value, type_check):
        pass

    # Shares its activation state qi=1 with its out-neighbors
    def bp(self,r):
        self.activation_history.append(self.qi)
        self.propagate(0)


# Normal follower class
class Followers(Agents):
    def __init__(self,id, value, F):
        super().__init__(id, F)
        self.xi = value
        self.history =[self.xi]

    # Reset its neighbor set, and sets q_i=0
    def neighbor_rest(self):
        self.connections = []
        self.q_i = 0

# Adversary class
class Adversary(Agents):
    def __init__(self,id, value, F =1):
        super().__init__(id,F)
        self.xi = value
        self.qi = randint(0,1)
        self.history =[self.xi]

    # If the type is 1, that means the value is a state xi. Otherwise, it is activation status qi
    def propagate(self, type_check=1):
        value = self.xi if type_check else self.qi
        for neigh in self.neighbors():
            neigh.receive(value,type_check)
    
    # Receive values from its neighbors: don't do anything
    def receive(self, value, type_check):
        pass

    # Arbitrarily update q_i only if q_i=0 and share it with its out-neighbors
    def bp(self,r, desired_qi=0):
        self.qi = desired_qi
        self.activation_history.append(self.qi)
        self.propagate(0)

    # Does not follow the nominal protocol 
    def w_msr(self):
        self.history.append(self.xi)

# Byzantine agent class
class Byzantine(Adversary):
    def __init__(self, id, F=1):
        super().__init__(id,F)
        self.time = 0
        self.xi =randint(-1,1)*1000
        self.history = [self.xi]

    # If the type is 1, that means the value is a state xi. Otherwise, it is activation state qi.
    # It sends a value of 1000*sin((t+j)/5) to its out-neighbor with j 
    def propagate(self, type_check=1):
        self.time+=1
        if type_check:
            for neigh in self.neighbors():
                self.xi = -1000*np.sin((self.time+neigh.id)/5)
                neigh.receive(self.xi, type_check)
        else:
            for neigh in self.neighbors():
                neigh.receive(self.qi, type_check)        

    # Do not follow the nominal protocol
    def w_msr(self):
        self.history.append(self.xi)
        self.Q_i = []
    


## Network class that takes a list of agents, number of leaders, and number of followers. 
## It performs BP-MSR, SW-MSR, and W-MSR
class Network():
    def __init__(self, agents, num_agents, num_leaders,F):
        self.agents = agents
        self.num_leaders = num_leaders
        self.num_followers = num_agents -  num_leaders
        self.num_agents = num_agents
        self.F = F
    
    # Connect agents within the network:
    def connect_network(self, graph):
        for (i,j) in graph:
            self.agents[i].connect([self.agents[j]])

    # Initialize and connect adversaries to the network
    def connect_adversaries(self):
        adversaries = []
        for f in range(self.F):
            adv = Byzantine(100 + f) 
            for i in range(self.num_leaders, self.num_agents):
                adv.connect([self.agents[i]])
            adversaries.append(adv)

        self.full_network = self.agents + adversaries
    
    # Update the leaders' states every given time step 
    def update_leader_states(self, new_value, t, step=50):
        if t % step == 0 and t > 0:
            for i in range(self.num_leaders):
                self.agents[i].xi = new_value


    # Performs the BP-MSR for all agents
    def BP_MSR(self, input=None):
        # First step: running Bootstrap Percolation (BP)
        for _ in range(self.num_followers+1):
            for aa in self.full_network:
                if aa.id >= 100 and input!= None:
                    aa.bp(2*self.F+1, input)
                    continue
                aa.bp(2*self.F+1)

        # Second step: share and update its states if q_i[t]=1. Otherwise, sleep through
        for aa in self.agents:
            aa.propagate()
        for aa in self.agents:  
            aa.bp_msr()
        for aa in self.agents:
            aa.neighbor_rest()
        
    # Performs the W-MSR for all agents:
    def W_MSR(self):
        for aa in self.agents:
            # Make sure all agents share their states x_i[t] with out-neighbors
            aa.qi = 1
            aa.propagate()
        for aa in self.agents:  
            aa.w_msr()
        for aa in self.agents:
            aa.neighbor_rest()


    # Performs the SW-MSR for all agents:
    def SW_MSR(self,t, T):
        for aa in self.agents:
            # Make sure all agents share their states x_i[t] with out-neighbors
            aa.qi = 1
            aa.propagate()
        for aa in self.agents:  
            aa.sw_msr(t,T)
        for aa in self.agents:
            aa.neighbor_rest()