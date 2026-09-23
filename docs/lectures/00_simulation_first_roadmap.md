# Lecture 00: Simulation-First Roadmap

## Learning Goals

After this lecture, the reader should be able to:

- identify which layer owns simulated events and which layer chooses actions;
- explain why one policy decision can span several simulator events;
- verify that Python imports the local GrADyS-SIM checkout;
- run the first no-RL trace and name its recorded outputs.

## Problem Background

The research object is an event-driven UAV edge intelligence scenario with
interchangeable decision policies. Tasks arrive, UAVs move, deadlines expire,
and service completes in simulated time. A learning algorithm sees this process
only through a chosen control boundary.

The teaching sequence is:

```text
simulator semantics -> scenario lifecycle -> measurable no-RL policy
                    -> RL formulation -> algorithm -> evaluation
```

## Theory: Events And Decisions

Let \(\tau_n\) denote the simulated time of event \(n\), and let \(t_k\)
be the time of control decision \(k\). At \(t_k\), a policy selects action
\(a_k\). The scenario requests an advance of `control_interval` \(\Delta\)
and returns an observation and reward after the simulator processes events:

\[
(o_{k+1},r_k,d_k)=F_{\Delta}(x_k,a_k,\xi_k).
\]

Here \(x_k\) is the simulator and scenario state, \(\xi_k\) collects sampled
workload and event outcomes, and \(d_k\) indicates episode completion. The
control index \(k\) is not an event index \(n\): several events may occur
during one decision interval. The current bridge repeatedly executes whole
events until simulated time reaches or exceeds the requested boundary. Thus
\(t_{k+1}\) can be slightly greater than \(t_k+\Delta\), including at the
configured episode duration. We will inspect this implementation in
[Lecture 01](01_gradys_core_in_aeroedge.md).

An RL objective may later use discounted return,

\[
G_k = \sum_{j=0}^{T-k-1} \gamma^j r_{k+j},
\]

where \(T\) counts control decisions in an episode. Its interpretation depends
on how the scenario aggregates events into \(r_k\), when the episode ends,
and what information appears in \(o_k\).

## AeroEdgeRL Contract

AeroEdgeRL preserves the GrADyS-SIM discrete-event core:

```text
SimulationBuilder
  -> SimulationConfiguration
  -> handlers
  -> protocol-backed nodes
  -> step_simulation / simulated time
```

The current `GradysUAVServiceCoreEnv` wraps this simulator and defines UAV
task arrivals, candidate selection, rewards, episode boundaries, and metrics.
Gymnasium, PettingZoo, RLlib, and future AgileRL integrations adapt the
scenario to training APIs.

| Owner | Input | Output |
| --- | --- | --- |
| GrADyS-SIM core | Nodes, handlers, scheduled events, protocol commands | Advanced simulated time and node state. |
| AeroEdgeRL scenario | Configuration, seed, UAV actions | Observations, rewards, done flags, metrics. |
| Heuristic or RL policy | Available decision information | UAV action indices. |
| Experiment runner | Scenario and policy | Traces and episode summaries. |

## Teaching Stack

```mermaid
flowchart TD
    A["GrADyS discrete-event simulator"] --> B["AeroEdgeRL scenario"]
    B --> C["No-RL rule-based policies"]
    C --> D["Metrics and traces"]
    D --> E["Tabular RL"]
    E --> F["Deep RL"]
    F --> G["RLlib MARL"]
```

## Minimal Runnable Example

Use the clean `aeroedge-rl` environment with editable installs of AeroEdgeRL
and the local `gradys-sim-nextgen` checkout. The first check is:

Run:

```bash
conda activate aeroedge-rl
cd /Users/wupengfei/Documents/Framework4test/AeroEdgeRL
python scripts/check_environment.py
```

The script prints the Python executable and version, `aeroedge_rl` version,
`gradysim` and mobility-module paths, and finally:

```text
Environment check passed.
```

When a sibling `gradys-sim-nextgen` directory exists, the script checks that
`gradysim` was imported from it. On another host, set
`AEROEDGE_GRADYSIM_ROOT` to the absolute local checkout path to enforce the
same check. It also checks for
`DynamicVelocityMobilityConfiguration`. A passing check confirms import
provenance and this required API; it is not a simulator behavior test.

Then run one short no-RL trace:

```bash
python -m aeroedge_rl.experiments.cli.no_rl_demo \
  --policy nearest \
  --seed 7 \
  --num-uavs 1 \
  --num-devices 5 \
  --episode-duration 12 \
  --candidate-limit 3 \
  --output /tmp/aeroedge_no_rl_nearest.jsonl
```

## Simulation Effect

The command prints a line for each control step with simulated time, selected
actions, reward sum, pending task count, hits, and misses. It writes a JSONL
trace containing action masks, candidate task IDs, reward values, and metric
snapshots. Add `--plot-output /tmp/aeroedge_no_rl_nearest.png` to save a
trajectory plot; the JSONL trace includes positions before and after each
decision interval.

Success here means the environment imports correctly and the decision loop
runs to an episode ending. It does not establish that `nearest` meets
deadlines, that trajectories are interpretable, or that RL will improve the
result. Lectures 03 and 04 add heuristic comparisons and trajectory inspection.

## Common Mistakes

- Treating `control_interval` as the spacing between individual simulator
  events; it is the requested interval between policy decisions.
- Trusting an import from an older installed `gradysim` package because the
  Python import itself succeeds.
- Reading one short trace as a policy comparison or research result.
- Assuming the nominal episode duration is an exact stop timestamp; the
  event-wise bridge can step past it by one event.

## Next Step

Continue to [Lecture 01: GrADyS Core In AeroEdgeRL](01_gradys_core_in_aeroedge.md)
to inspect how the scenario builds and advances the event-driven simulator.
