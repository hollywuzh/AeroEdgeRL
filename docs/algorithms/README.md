# Algorithms

This section records how reinforcement-learning algorithms should be reproduced
inside AeroEdgeRL.

The goal is not to collect algorithm names. Each algorithm should be connected
to a concrete scenario, a clear input/output contract, and a reproducible
experiment.

## Reproduction Principle

For every algorithm, document:

- theoretical objective;
- state, action, reward, and transition assumptions;
- single-agent or multi-agent setting;
- required simulator interface;
- expected input tensors or dictionaries;
- expected output actions or policies;
- compatible scenario family;
- heuristic baseline to compare against;
- smallest runnable experiment;
- failure modes and diagnostics.

## Algorithm Path

The recommended path is:

```text
tabular foundations
  -> value prediction
  -> value control
  -> function approximation
  -> policy gradient
  -> actor-critic
  -> deep RL
  -> multi-agent RL
```

This path keeps the lectures mathematically grounded while still moving toward
RLlib and AgileRL experiments.

## Initial Algorithm Backlog

Initial single-agent backlog:

- dynamic programming;
- Monte Carlo prediction and control;
- temporal-difference learning;
- SARSA;
- Q-learning;
- DQN;
- policy gradient;
- actor-critic;
- PPO.

Initial multi-agent backlog:

- independent Q-learning;
- independent PPO;
- shared-policy PPO;
- centralized training with decentralized execution;
- MAPPO-style centralized critic.

## AeroEdgeRL Mapping

Every algorithm should eventually answer:

```text
What does this algorithm need from the simulator?
What does the simulator return to the algorithm?
Which part is generic RL, and which part is scenario-specific?
```

This prevents the project from becoming a pile of training scripts.
