# Evaluation Protocol

AeroEdgeRL evaluation combines metrics, baselines, and visual inspection.

For the first [static sensor TSP](../scenarios/static_sensor_tsp.md), compare
route validity, closed-tour length, executed distance/time, inference time,
and trajectory on the same held-out instances. Task hits, misses, SLOs,
queues, and dynamic arrivals belong to later scenarios.

## Minimum Evaluation Checklist

For a scenario-level result, record:

- same random seeds;
- same scenario configuration;
- same episode duration;
- same workload distribution;
- same metrics table;
- random baseline;
- at least one heuristic baseline;
- RL policy result;
- multiple-seed mean and variance;
- UAV trajectory visualization.

## Trajectory Validity

Trajectory visualization is part of evaluation.

The plot should help answer:

- are UAVs moving toward meaningful task or service regions?
- do trajectories reflect scenario dynamics?
- are paths dominated by chaotic crossings?
- do multiple UAVs collapse into the same route without reason?
- does a learned policy behave differently from the heuristic baseline?

If the visualization is not interpretable, the experiment should not be treated
as a trustworthy research result yet.

## Baseline Rule

RL should not be evaluated alone.

Every RL experiment should be compared against:

- random valid policy;
- at least one scenario-specific heuristic;
- when possible, a stronger domain baseline.
