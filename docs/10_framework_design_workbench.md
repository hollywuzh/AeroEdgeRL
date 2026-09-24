# Framework Design Workbench

This document is the local design workbench for AeroEdgeRL. It is intentionally
more exploratory than the formal architecture documents. Ideas should be tested
here first, refined through local MkDocs preview, and only later promoted into
stable project documents or implementation tasks.

## First Principle

AeroEdgeRL is not a thin wrapper around RLlib, Gymnasium, PettingZoo, or
AgileRL.

Its purpose is to express low-altitude UAV edge-intelligence problems as
reproducible, extensible, and interpretable discrete-event reinforcement
learning experiments.

The framework must preserve the GrADyS-SIM discrete-event simulation core. RL
libraries are training backends and interface targets. They do not define the
simulator semantics.

## Research-Scenario Expansion Principle

AeroEdgeRL should continuously expand its research scenarios.

Each scenario should follow a staged path:

```text
scenario modeling
  -> no-RL simulation demo
  -> heuristic minimal closed loop
  -> RL environment formulation
  -> RL reproduction
  -> RL improvement and ablation
```

This staged path is mandatory because a scenario is not research-ready just
because an RL agent can be attached to it. The project should first prove that
the scenario dynamics, metrics, and evaluation loop make sense without RL.

## Scenario Development Rule

For every new scenario, implement the simplest useful heuristic before training
an RL policy.

The heuristic does not need to be optimal. It should be:

- deterministic or seed-controlled;
- easy to explain;
- fast to run;
- strong enough to expose whether the simulator loop, metrics, and termination
  conditions are working;
- weak enough that an RL method has room to improve.

Only after the heuristic loop is stable should the scenario be wrapped for RL
training.

## Why Heuristics Come First

Heuristic baselines serve four roles.

First, they validate the simulator. If a nearest-server, earliest-deadline, or
greedy-energy policy produces nonsensical trajectories or metrics, the RL setup
is probably not ready.

Second, they define the minimum closed loop. A scenario should be runnable from
configuration to metrics without any neural-network dependency.

Third, they provide interpretable baselines. RL results should be compared
against policies that domain researchers can understand.

Fourth, they make teaching easier. A lecture can introduce the scenario through
the heuristic loop before adding value functions, policy gradients, or
multi-agent learning.

## Scenario Template

Each scenario should eventually answer these questions.

### Problem

What is being optimized?

Examples:

- task completion ratio;
- service latency;
- SLO violation rate;
- UAV energy consumption;
- communication coverage;
- age of information;
- resilience under failures or attacks.

### World

What entities exist in the simulation?

Examples:

- UAVs;
- ground devices;
- edge servers;
- base stations;
- service requests;
- network links;
- obstacles or no-fly zones;
- adversarial nodes.

### Events

Which events drive the discrete-event simulator?

Examples:

- task arrival;
- task deadline expiration;
- UAV mobility update;
- communication state update;
- service completion;
- battery update;
- link failure;
- attack launch.

### Actions

What does the controller decide?

Examples:

- assign a task to a UAV;
- move toward a waypoint;
- select an edge server;
- choose transmit power;
- decide whether to offload or process locally;
- re-route under link degradation.

### Observations

What can each agent observe?

The scenario should distinguish:

- local observation;
- global state;
- privileged training-only state;
- metric-only state.

### Rewards

What reward is used for RL?

The reward should be derived from scenario metrics, not invented independently.
If the reward cannot be explained to a domain reader, it is probably too
fragile.

### Heuristic Baselines

What is the first non-RL closed-loop policy?

Examples:

- random valid action;
- nearest-server assignment;
- earliest-deadline-first scheduling;
- shortest-processing-time-first scheduling;
- greedy SLO-risk reduction;
- greedy energy-aware routing;
- patrol or coverage sweep.

### RL Reproduction

Which RL setting reproduces the same control problem?

Examples:

- single-agent centralized PPO through Gymnasium;
- multi-agent shared-policy PPO through RLlib;
- PettingZoo parallel environment for independent UAV policies;
- AgileRL experiments in a separate environment.

### Evaluation

How do we know the result is meaningful?

At minimum:

- same random seeds;
- same scenario configuration;
- same episode duration;
- same workload distribution;
- same metrics table;
- heuristic versus RL comparison;
- multiple-seed mean and variance for training results;
- valid UAV trajectory visualization, meaning the rendered trajectories should
  be interpretable and consistent with the scenario dynamics rather than a
  chaotic set of crossing lines.

## First Formal Scenario

The first formal teaching scenario is a
[static sensor TSP](scenarios/static_sensor_tsp.md): one UAV, one depot,
mandatory visits to fixed sensors, and return to the depot. It minimizes a
closed Euclidean tour. Task value, deadlines, queues, arrivals, offloading,
and communication decisions are excluded at this stage.

Initial closed loop:

```text
seeded depot/sensor instance
  -> nearest-neighbor and 2-opt tours
  -> validate complete permutation
  -> GrADyS route execution and visit events
  -> compare planned length, executed distance/time, and trajectory
```

Track A later chooses one next unvisited sensor at a time; Track B learns a
complete permutation before departure. Both are evaluated on the same TSP
instances. The dynamic `uav_edge_service` code is the first implemented
framework prototype and remains available for later research scenarios.

## Candidate Scenario Backlog

The framework should expand beyond one benchmark.

Candidate scenarios:

- UAV data collection with age-of-information objectives;
- post-disaster edge sensing and service recovery;
- UAV-assisted mobile edge computing with task offloading;
- low-altitude sensing-communication-computation integration;
- multi-UAV coverage and service patrol;
- network security and adversarial routing;
- training-inference separation for UAV edge intelligence;
- ECaaS/DaaS service orchestration under low-altitude mobility.

Each candidate must still follow the same rule:

```text
heuristic minimal closed loop first, RL reproduction second
```

## Immediate Design Questions

The next design questions are:

1. What exactly happens during one RL step?
2. Does an RL step advance the simulator by a fixed control interval, by event
   count, or until the next decision event?
3. Which metrics are scenario-native, and which are only RL diagnostics?
4. Which heuristic should be the first strong baseline for UAV edge service?
5. What is the smallest PPO experiment that is meaningful enough for Windows
   GPU validation?

These questions should be resolved before adding more algorithms.
