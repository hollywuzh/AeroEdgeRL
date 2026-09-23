# Project Charter

## Name

AeroEdgeRL

Recommended repository name:

```text
aero-edge-rl
```

Recommended Python package name:

```text
aeroedge_rl
```

## Mission

AeroEdgeRL is a research-oriented simulation framework for UAV-assisted edge
intelligence and multi-agent reinforcement learning. It combines event-driven
network simulation with standard RL interfaces so that UAV mobility, wireless
communication, edge-service workloads, energy models, and SLO-aware scheduling
can be studied in one reproducible environment.

## First Principle

The framework must preserve the discrete-event simulation core inherited from
GrADyS-SIM.

This means:

- Simulated time is advanced by an event loop, not by an RL library.
- Nodes, handlers, mobility, communication, timers, and telemetry remain
  simulator-level concepts.
- RL step semantics are built on top of simulator advancement.
- Gymnasium, PettingZoo, RLlib, and AgileRL are adapters, not the core engine.

## Scope

In scope:

- UAV mobility and swarm control.
- Edge-device task generation and service orchestration.
- Multi-agent RL and centralized/decentralized control.
- Event-driven network and mobility simulation.
- Benchmark scenarios, baselines, metrics, visualization, and reproducibility.

Out of scope for the first phase:

- Replacing GrADyS-SIM's event system.
- Building a custom RL algorithm library from scratch.
- Tightly coupling the core simulator to one RL backend.
- Prematurely supporting every possible network or UAV physics model.

## Success Criteria

The first usable version should provide:

- A reusable core environment independent of Gymnasium/RLlib/AgileRL imports.
- A Gymnasium adapter for centralized single-controller experiments.
- A PettingZoo parallel adapter for multi-agent experiments.
- An RLlib MultiAgentEnv adapter for scalable PPO/IPPO-style training.
- A documented path for AgileRL integration.
- Baseline policies and reproducible experiment scripts.
- Tests showing that one RL control step advances the GrADyS event simulation
  correctly.

