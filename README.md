
# Overview
This repository provides the implementation of resilient leader-follower consensus simulations from our paper "Partial Resilient Leader-Follower Consensus in Time-Varying Graphs." 

Many standard resilient consensus algorithms, particularly MSR-type algorithms, rely on robustness conditions of the entire network, such as strong r-robustness. However, these robustness conditions (i) are difficult for each agent to verify with its local information and (ii) typically require dense network structures, which can be challenging to maintain in real systems. Despite these challenges, the behavior of consensus systems when **robustness conditions of the entire network do not hold** has been largely unexplored. In our work, we introduce the notion of **partial leader-follower consensus**, where a subset of normal (non-adversarial) followers is guaranteed to track the leader’s reference state, even if the network does not satisfy full robustness conditions. 

We propose a novel distributed algorithm, BP-MSR, that allows a subset of normal follower to achieve leader-follower consensus in arbitrary sequence of time-varying networks with a bounded number of adversaries. Unlike previous work that relies on global network robustness to guarantee convergence of all followers, our approach provides sufficient conditions for convergence at the level of individual followers, allowing us to explicitly characterize which followers will converge.

## Key Contributions of Our Paper
- **BP-MSR algorithm**: A fully distributed algorithm that combines Bootstrap Percolation (BP) and the Mean Subsequence Reduced (MSR) approach.
- **Convergent Set Analysis**: Sufficient conditions for convergence provided for each individual follower, allowing explicit identification of the convergent set.
- **Simulation Results**: Simulations demonstrating that BP-MSR algorithm guarrantees partial consensus, even when traditional resilient consensus algorithms fail to do so.


## In This Repo
This repository provides the BP-MSR algorithm implementation and simulations for resilient leader-follower consensus. The simulations illustrate (i) comparison between BP-MSR and traditional MSR-type algorithms and (ii) empiricial validation of the subsets and supersets of the convergent set characterized in the paper.
- `simulation.py` - Main script to run consensus simulation.
- `Agents.py` - Agent and network classes implementing BP-MSR and other consensus methods.
- `simulator.py` - Helper script for simulation execution.
- `requirements.txt` - Python dependencies.

## How to Use
- Run `simulation.py` to run the simulation
- Optional: Modify the network topology in the `simulation.py` script to observe different consensus behaviors

  

