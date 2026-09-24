# Scenarios

Scenarios are first-class research objects in AeroEdgeRL. The initial teaching
sequence starts from a distilled combinatorial optimization problem and adds
domain components only after that problem can be solved and executed.

The framework should not be organized around a single algorithm or a single
benchmark. It should continuously expand a family of UAV edge-intelligence
scenarios, and each scenario should be validated before RL training is treated
as meaningful.

## Scenario Lifecycle

Every scenario follows the same lifecycle:

```text
combinatorial problem definition
  -> no-RL simulation demo
  -> heuristic minimal closed loop
  -> interactive or route-learning formulation
  -> RL reproduction on the same instances
  -> RL improvement and ablation
```

The heuristic loop is mandatory. It proves that the simulator, metrics,
termination rules, and visualization pipeline are coherent before neural
policies are introduced.

## Required Scenario Artifacts

Each scenario should eventually provide:

- problem definition;
- simulated entities;
- event model;
- action space;
- observation model;
- reward design;
- heuristic baselines;
- RL adapter mapping;
- evaluation protocol;
- trajectory visualization;
- reproducible smoke command.

## Evaluation Standard

A scenario is not considered ready only because training runs without crashing.

It should also satisfy:

- reproducible seeds;
- comparable heuristic and RL policies;
- clear metrics;
- valid UAV trajectory visualization;
- interpretable behavior under the no-RL and heuristic baselines.

If the trajectory visualization is a chaotic set of crossing lines with no
scenario-level meaning, the scenario still needs modeling work.

## Current Scenario Family

The first formal teaching scenario is:

- [Static Sensor TSP](static_sensor_tsp.md) (planned implementation).

An earlier [UAV Edge Service](uav_edge_service.md) prototype is runnable and
kept for later dynamic-scenario research. It is outside the initial TSP
teaching sequence.
