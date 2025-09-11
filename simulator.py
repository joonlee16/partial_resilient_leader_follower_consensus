import numpy as np
import matplotlib.pyplot as plt
from Agents import *
from copy import deepcopy
from random import randint


'''This script contains all the main functionalities for the consensus simulations
'''

# Plot the results for the resilient consensus (blue for leaders, green for followers, and red for adversaries)
def plotter(network_groups, time, algorithm, **kwargs):
    """
    network_groups: list of 3 lists (each list is a set of agents for one subplot)
    time: int, number of timesteps
    algorithm: str, title for the figure
    """
    dim1, dim2, figsize = kwargs.values()
    fig, axes = plt.subplots(dim1, dim2, figsize=figsize,  sharex=True)
    t = range(0, time+1)

    for idx, (ax, network) in enumerate(zip(axes, network_groups)):
        # Plot reference trajectory
        ax.plot(t, [1000*np.sin((i+5)/5) for i in t], "r--", linewidth=2, label="Reference")

        # Plot agents
        for agent_ in reversed(network):
            if isinstance(agent_, Followers):
                color = "g"
            elif isinstance(agent_, Adversary):
                color = "r"
            else:  # Leaders
                color = "b"
            ax.plot(t, agent_.history, color, linewidth=2)

        ax.set_ylabel("Consensus State", fontsize=12)
        ax.set_title(algorithm[idx], fontsize=15)
        ymin, ymax = ax.get_ylim()
        ax.set_yticks(np.linspace(ymin, ymax, 5))  # ~6 ticks per subplot
        ax.tick_params(axis='y', labelsize=15)

    axes[-1].set_xlabel("Time", fontsize=15)
    axes[-1].tick_params(axis='x', labelsize=15)

    fig.tight_layout()
    plt.show()

# Initialize the agents
def initialize_agents(num_leaders, num_agents, F, given_value=0):
    leaders = [Leaders(i, given_value, F) for i in range(num_leaders)]
    followers = [Followers(i, randint(-1000, 1000), F) for i in range(num_leaders, num_agents)]
    return leaders, followers

# For each network, (1) update the leaders' value if applicable, and (2) connect the adversaries to the network
def update_and_connect(networks, t, step=50):
        new_value = np.random.randint(-1000, 1000)
        for net in networks:
            # The leaders update their reference states every 50 time steps
            net.update_leader_states(new_value, t, step=step)
            # Initialize and connect the Byzantine agents to the network
            net.connect_adversaries()


# Main simulation function
def leader_scalar_resilient_consensus(num_leaders, num_agents, F, time, graphs):
    print("running simulations with", num_agents, "agents,", num_leaders, "leaders, and", F, "-local adversaries")

    # Initialize leaders and followers
    leaders, followers = initialize_agents(num_leaders, num_agents, F, given_value=0)

    # Initialize 3 different networks with the same initial conditions to compare performance of different resilient consensus algorithms:
    # network1: BP-MSR, network2:W-MSR, network3: SW-MSR
    net1 =  leaders + followers
    net2 = deepcopy(net1)
    net3 = deepcopy(net1)
    
    network1 = Network(net1, num_agents, num_leaders, F)
    network2 = Network(net2, num_agents, num_leaders, F)
    network3 = Network(net3, num_agents, num_leaders, F)

    
    # Initialize the activation state vectors
    sum_of_qis = np.zeros(num_agents)

    # Retrieve the Gcal_1 and Gcal_2
    gcal_1, gcal_2 = graphs
    edges_list = [gcal_1, gcal_2]
    # Finding the union of Gcal_1 an Gcal_2
    combined_edges = np.vstack((gcal_1, gcal_2))
    union_graph = list(set(tuple(edge) for edge in combined_edges))

    # Main simulation loop
    for t in range(time):
        
        # Graph sequence where the two graphs Gcal_1 and Gcal_2 repeat periodically
        graph_sequence1 = edges_list[t % len(edges_list)]

        # Graph sequence of one graph which is formed by the union of Gcal_1 and Gcal_2
        graph_sequence2 = union_graph

        # Agents form connections based on the given graph
        # Network1 and network2 use graph_sequence1, and network3 uses graph_sequence2
        network1.connect_network(graph_sequence1); network2.connect_network(graph_sequence1)
        if t<2: 
            network3.connect_network(graph_sequence1) 
        else: 
            network3.connect_network(graph_sequence2)

        # The leaders update their reference states every 50 time steps
        # Initialize and connect the Byzantine agents to the network
        update_and_connect([network1, network2, network3], t, step=50)

        # Each agent in network1, network2, and network3 runs the BP-MSR, W-MSR, and SW-MSR, respectively
        network1.BP_MSR()
        network2.W_MSR()
        network3.SW_MSR(t, T=2)
            
        # Record the activation status of each agent
        sum_of_qis+=np.array([aa.qi for aa in network1.agents])

    print("Sum of Acitvations across iterations:", sum_of_qis)

    # Plot the results for the resilient consensus
    plotter([network2.agents, network3.agents, network1.agents], time, ["W-MSR","SW-MSR", "BP-MSR"], dim1=3, dim2=1, figsize=(10, 6))



# Main simulation function
# Compare performance of BP-MSRs depending on the behaviors of advesaries in updating and sharing their activation states

def leader_scalar_resilient_consensus2(num_leaders, num_agents, F, time, edges_list):
    print("running simulations with", num_agents, "agents,", num_leaders, "leaders, and", F, "-local adversaries")

    # Initialize leaders and followers
    leaders, followers = initialize_agents(num_leaders, num_agents, F, given_value=0)
    # Initialize 2 different networks with the same initial conditions to compare performance of BP-MSRs depending on the 
    # behaviors of advesaries in updating and sharing their activation states
    # Network1: when all adversaries i \in \Acal share q_i[t,k]=0 for all t and k
    # Network2: when all adversaries i \in \Acal share q_i[t,k]=1 for all t and k

    network1 =  leaders + followers
    network2 = deepcopy(network1)

    network1 = Network(network1, num_agents, num_leaders, F)
    network2 = Network(network2, num_agents, num_leaders, F)

    # Initialize the activation state vectors
    sum_of_qis = np.zeros(num_agents)
    sum_of_qis2 = np.zeros(num_agents)

    # Main simulation loop
    for t in range(time):
        # Graph sequence where the two graphs Gcal_1 and Gcal_2 repeat periodically
        graph_sequence = edges_list[t % len(edges_list)]

        # Agents form connections based on the given graph
        # Network1 and network2 use graph_sequence
        network1.connect_network(graph_sequence)
        network2.connect_network(graph_sequence)

        # The leaders update their reference states every 50 time steps
        # Initialize and connect the Byzantine agents to the network
        update_and_connect([network1, network2], t, step=50)

        # Each agent in network1 and network2 runs the BP-MSR
        # All advesaries i \in \Acal share q_i^j[t,k]=0 with its out-neighbors j in network1
        # All advesaries i \in \Acal share q_i^j[t,k]=1 with its out-neighbors j in network2
        network1.BP_MSR(0)
        network2.BP_MSR(1)

        # Record the activation status of each agent
        sum_of_qis+=np.array([aa.qi for aa in network1.agents])
        sum_of_qis2+=np.array([aa.qi for aa in network2.agents])

    print("Case 1: sum of activations when all advesaries share q_i[t,k]=0:", sum_of_qis)
    print("Case 2: sum of Acitvations when all advesaries share q_i[t,k]=1:", sum_of_qis2)


    # Plot the results for the resilient consensus
    plotter([network1.agents,network2.agents], time, ["Min Convergent Set", "Max Convergent Set"], dim1=2, dim2= 1, figsize=(10, 6))




