# UAV Edge Service

The UAV edge service scenario is an existing dynamic framework prototype.
The first formal teaching problem is the
[Static Sensor TSP](static_sensor_tsp.md); this prototype is retained for
later edge-service research and adapter checks.

Its purpose is to study how UAV agents assist edge-service orchestration under
task arrivals, mobility, deadlines, and service-quality constraints.

## Minimal Closed Loop

The initial closed loop is:

```text
ground devices generate service tasks
  -> UAVs observe pending tasks and candidate service targets
  -> a heuristic policy assigns, ignores, or delays tasks
  -> the discrete-event simulator advances
  -> tasks complete or miss deadlines
  -> metrics and UAV trajectories are recorded
```

## First Heuristic Baselines

The first baseline set should include:

- random valid assignment;
- nearest feasible service target;
- earliest-deadline-first;
- greedy SLO-risk reduction.

These baselines should run without RLlib, Torch, or Ray. They are the scenario
sanity checks.

## RL Reproduction Path

After the heuristic loop is stable, reproduce the same decision problem through:

- Gymnasium centralized PPO smoke tests;
- PettingZoo parallel multi-agent rollout;
- RLlib shared-policy PPO;
- later IPPO/MAPPO-style variants.

## Visualization Requirement

Every experiment should be able to produce UAV trajectory data.

The rendered trajectory should help answer:

- did UAVs move toward meaningful service regions?
- did the policy create unnecessary oscillation?
- did multiple UAVs collapse into the same route?
- do crossings reflect valid task/service interactions or only controller
  noise?

The trajectory plot is part of evaluation, not a decoration.
