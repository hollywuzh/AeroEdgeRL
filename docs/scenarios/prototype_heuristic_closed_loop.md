# Prototype: Heuristic Closed Loop

This page evaluates the existing dynamic edge-service prototype. The first
formal teaching problem is the [Static Sensor TSP](static_sensor_tsp.md).

## Learning Goals

After this prototype, you should be able to trace a decision from candidate tasks
through a rule-based policy, a GrADyS-SIM control interval, and an episode metric.
You should also be able to compare policies under the same generated workload.

## Problem Background

At control time \(t\), UAV \(u\) sees at most \(K\) pending candidate tasks.
It chooses action \(0\) (hover or retain the current target) or action
\(j\in\{1,\ldots,K\}\) (select candidate \(j\)). The environment requests
an advance of one `control_interval`; event-wise execution can step slightly
beyond it. Task arrivals, expiry, movement, and service completion occur in
simulated time. The next candidate list may differ.

The minimal closed loop is:

```text
reset(seed) -> candidate tasks -> policy(env, rng) -> actions
            -> env.step(actions) -> rewards, metrics, next candidates -> repeat
```

## Theory

Let \(\mathcal C_u(t)\) be the visible candidate list for UAV \(u\), and
\(d(u,i)\), \(D_i\), and \(c_i\) denote distance, absolute deadline, and
compute demand for task \(i\). The implemented rules are:

| Policy | Decision rule when candidates exist | Diagnostic role |
| --- | --- | --- |
| `hover` | \(a_u=0\) | Inactive reference. |
| `random` | Uniformly sample from actions allowed by `action_mask`. | Valid-action stochastic reference. |
| `nearest` | \(\arg\min_{i\in\mathcal C_u(t)} d(u,i)\) | Movement-aware heuristic. |
| `edf` | Select the first candidate, ordered by deadline and then distance by the environment. | Deadline-only heuristic. |
| `slo-risk` | \(\arg\min_i [D_i-t-d(u,i)/v_{\max}-c_i/\mu]\) | Approximate service-risk heuristic. |

Here \(v_{\max}\) is configured horizontal speed and \(\mu\) is compute
rate. The SLO-risk score is an estimate, not a guarantee of meeting a deadline:
it omits contention, communication time, and future arrivals. A negative score
means the simple travel-plus-compute estimate already exceeds the time left.

Candidate indices are local to a UAV and may change after each step. For
`nearest` and `slo-risk`, Python list index \(i\) maps to action \(i+1\).
All policies return \(0\) when the UAV cannot select a new task. This includes
busy UAVs and UAVs with an active target, even if other tasks are visible.

## AeroEdgeRL Contract

| Stage | Input | Output |
| --- | --- | --- |
| Reset | `UAVServiceEnvConfig`, episode seed | Initial simulator state and observations. |
| Policy | `GradysUAVServiceCoreEnv`, policy RNG | `{agent_id: action_index}` for each UAV. |
| Step | Action dictionary | New observations, per-agent rewards, termination/truncation. |
| Evaluation | Step rewards and `metrics_snapshot()` | Episode return, hits, misses, pending tasks, energy, queue statistics. |

The policy currently reads `candidate_tasks`, `agent_position`, `time`, and
configuration directly from the core environment. This is a heuristic
baseline interface, not the observation-only contract promised to an RL
policy. When comparing an RL agent with a heuristic, document which
information each policy can access.

## Minimal Runnable Example

Activate the local environment and confirm that `gradysim` resolves to the
local sibling checkout:

```bash
conda activate aeroedge-rl
cd /Users/wupengfei/Documents/Framework4test/AeroEdgeRL
python scripts/check_environment.py
```

Trace one policy step by step:

```bash
python -m aeroedge_rl.experiments.cli.no_rl_demo \
  --policy slo-risk \
  --seed 7 \
  --num-uavs 1 \
  --num-devices 5 \
  --episode-duration 12 \
  --candidate-limit 3 \
  --output /tmp/aeroedge_slo_risk_trace.jsonl \
  --plot-output /tmp/aeroedge_slo_risk_trajectory.png
```

The JSONL file records `time`, `actions`, `action_masks`, `reward_sum`,
`metrics`, `candidate_task_ids`, and UAV positions for every control step.
The mask and candidates are from before the action. The PNG shows the sampled
path with start and end points, ground devices, and simulated-time color.

Compare episode summaries:

```bash
python -m aeroedge_rl.experiments.cli.baselines \
  --episodes 3 \
  --seed 7 \
  --num-uavs 1 \
  --num-devices 5 \
  --episode-duration 20 \
  --candidate-limit 3 \
  --policies hover,random,nearest,edf,slo-risk \
  --csv-output /tmp/aeroedge_heuristic_baselines.csv
```

The CSV contains one row per policy and episode, including `seed`,
`total_reward`, `hits`, `misses`, `success_rate`, `miss_rate`,
`total_energy_used`, and queue statistics. Each policy is reset with the
same sequence of episode seeds (`7`, `8`, `9` here). This is a paired
scenario comparison, although stochastic policy decisions and subsequent
state-dependent event sequences can diverge.

## Simulation Effect And Evaluation

For episode \(e\), the runner accumulates the undiscounted step reward

\[
G_e=\sum_{t=0}^{T_e-1}\sum_{u\in\mathcal U}r_{u,t}.
\]

The printed `avg_reward` is \(N^{-1}\sum_e G_e\). `meanQ` is the mean of
the *post-step* pending-task counts within an episode, averaged across
episodes. `maxQ` is the episode maximum, averaged across episodes. These
figures measure different things: a policy can improve task hits while
spending more energy or leaving a larger queue.

`success_rate` is `hits / (hits + misses)` when that denominator is nonzero.
Pending tasks are excluded; a high displayed success rate with many pending
tasks is not evidence of high workload completion. For the example above,
the observed three-episode means were:

| Policy | Avg. reward | Avg. hits | Avg. pending queue | Avg. energy |
| --- | ---: | ---: | ---: | ---: |
| `hover` | -1.09 | 0.0 | 3.4 | 0.0 |
| `random` | 10.96 | 1.3 | 2.8 | 148.0 |
| `nearest` | 14.21 | 1.7 | 2.6 | 161.6 |
| `edf` | 7.35 | 1.0 | 2.8 | 176.0 |
| `slo-risk` | 7.35 | 1.0 | 2.8 | 176.0 |

These values are a reproducible sanity run with seeds 7-9, not a research
comparison. Their differences are small and the sample is only three episodes.

Inspect a result in this order:

1. Check generated work and whether `hover` leaves work pending or missed.
2. Compare `hits`, `misses`, and queue statistics across active policies.
3. Compare energy and reward; explain tradeoffs with the scenario reward.
4. Read a JSONL trace to connect selected actions to candidate IDs and
   subsequent metrics.
5. Inspect the generated UAV path before claiming a useful flight policy.
   Position samples alone cannot establish that crossings are meaningful.

Three short episodes are a functional comparison, not a statistical result.
The next experiment stage needs more seeds, uncertainty estimates, and
systematic trajectory inspection.

## Common Mistakes

- Treating `success_rate` as a fraction of all generated tasks; pending work
  is excluded from its denominator.
- Treating SLO-risk's approximate slack as actual deadline feasibility.
- Comparing only reward while ignoring hits, misses, queueing, and energy.
- Assuming equal seeds force identical task histories after policies cause
  different simulator states.
- Claiming trajectory quality without looking at the plotted path.

## Next Step

Continue to the [trajectory prototype](prototype_trajectory_data_and_visualization.md) to inspect
the recorded UAV path as part of scenario evaluation.
