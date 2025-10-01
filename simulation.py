import numpy as np
from simulator import leader_scalar_resilient_consensus,leader_scalar_resilient_consensus2

'''This script simulates resilient leader-follower consensus with different resileint consensus algorithms in time-varying graphs. 
We aim to show our presented algorithm Bootstrap Percolation +  Mean Susbsequence Reduced (BP+MSR) will allow a subset of followers to 
achieve partial resilient leader-follower consensus, regardless of the graph theoreitc robustness level of the underlying network.
For comparison, we have Weighted-MSR (W-MSR) and Sliding W-MSR (SW-MSR), which are shown to guarantee full leader-follower consensus as 
long as the global network satisfies certain robustness levels.
'''

# Number of adversaries, number of leaders, and number of all agents
F = 1
num_leaders = 2*F+1
num_agents = 9

# Simulation time 
time = 100

# Graph sequence Gcal_1, Gcal_2, Gcal_3 (only include normal agents)
gcal_1 = np.array([(4, 5), (0, 6), (1, 6), (2, 6), (8, 6), (3, 7), (0, 3), (4, 7), (8, 7), (2, 5), (0, 5), (6, 5), (8, 5)])
gcal_2 = np.array([(0, 7), (1, 7), (2, 7), (8, 4), (4,6), (8, 6), (8, 5), (3, 4), (1, 4), (8, 3)])
gcal_3 = np.array([(0, 5), (1, 5), (2, 5), (8, 5), (8, 3), (8, 4), (1, 3), (2, 3), (3, 4), (5, 4)])

# Simulation comparison with other resilient consensus algorithms and a squence of Gcal_1 and Gcal_2
leader_scalar_resilient_consensus(num_leaders, num_agents, F, time, [gcal_1, gcal_2])

# Simulation performance of BP+MSRs depending on the behaviors of advesaries in updating and sharing their activation states
leader_scalar_resilient_consensus2(num_leaders, num_agents, F, time, [gcal_1, gcal_2, gcal_3])

