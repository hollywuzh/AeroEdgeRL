# AeroEdgeRL Lecture Notes

The lecture notes are the guided learning path for AeroEdgeRL.

They teach how to move from discrete-event UAV simulation to a small,
well-defined combinatorial problem and its no-RL baselines. The first formal
example is a [static sensor TSP](../scenarios/static_sensor_tsp.md). Interactive
RL and combinatorial route RL are later research paths.

## How To Read These Notes

Read the lectures in this order:

```text
simulation first
  -> static TSP instance
  -> no-RL route baselines and GrADyS execution
  -> shared RL foundations
  -> interactive RL / combinatorial RL
  -> executed-scenario comparison and visualization
```

The [two-track design](research_tracks.md) records the agreed decision
interfaces and open modeling questions. An RL result is meaningful only after
the underlying scenario can be explained without RL.

## Course Map

| Part | Theme | Goal |
| --- | --- | --- |
| I | Static TSP Simulation First | Define a closed sensor tour, solve it without RL, and execute it in GrADyS-SIM. |
| II | Shared RL Foundations | Define decisions, observations, returns, and values before the two tracks diverge. |
| III | Interactive And Combinatorial RL | Teach step-action learning and structured route learning as parallel paths. |
| IV | Multi-Agent RL | Extend from one controller to multi-UAV learning. |
| V | Research Experiments | Turn a scenario and an algorithm into a research-grade experiment. |

### Part I: Static TSP Simulation First

| Lecture | Status | Purpose | Runnable artifact |
| --- | --- | --- | --- |
| [Course Design](lecture_design.md) | current | Define the structure and teaching contract of the lecture series. | MkDocs preview |
| [Two Research Tracks](research_tracks.md) | current | Record the agreed decision interfaces and the first teaching-instance gates. | Design contract |
| [Simulation-First Roadmap](00_simulation_first_roadmap.md) | current | Explain why AeroEdgeRL starts from simulation rather than RL training. | `scripts/check_environment.py` |
| [GrADyS Core In AeroEdgeRL](01_gradys_core_in_aeroedge.md) | current | Explain the preserved simulator and distinguish the existing dynamic prototype from the planned TSP executor. | `scripts/check_environment.py` |
| 02 Static Sensor TSP Contract | planned | Define depot, mandatory sensors, Euclidean tour, and simulator visit events. | [Scenario contract](../scenarios/static_sensor_tsp.md); executor planned |
| 03 No-RL TSP Solvers | planned | Use LKH as the primary heuristic baseline and nearest-neighbor as a sanity check. | [LKH adapter](../scenarios/static_sensor_tsp.md); simulator loop planned |
| 04 Route Execution And Visualization | planned | Execute routes in GrADyS and compare planned versus actual movement. | planned |
| Simulator Time Versus Wall-Clock Time | planned | Separate discrete-event simulated time from training runtime and logging time. | planned |

### Part II: Shared RL Foundations

| Lecture | Status | Purpose | Runnable artifact |
| --- | --- | --- | --- |
| MDP Formulation | planned | Map a decision boundary to state, action, reward, transition, and discount factor. | planned |
| Permutation Policy And Route Return | planned | Define route-construction actions, masking, terminal cost, and return for static TSP. | planned |
| Return And Value Functions | planned | Define return, state value, and action value in simulator-facing terms. | planned |
| Bellman Equations | planned | Derive Bellman expectation and optimality equations for the scenario. | planned |
| Dynamic Programming | planned | Reproduce policy evaluation and policy improvement in a small controlled setting. | planned |
| Monte Carlo Methods | planned | Estimate returns from sampled episodes. | planned |
| Temporal-Difference Learning | planned | Learn from partial episode transitions. | planned |
| SARSA | planned | Compare on-policy TD control with simulator-generated trajectories. | planned |
| Q-learning | planned | Compare off-policy TD control with heuristic baselines. | planned |

### Part III: Interactive And Combinatorial RL

Track A learns actions through simulator interaction:

| Lecture | Status | Purpose | Runnable artifact |
| --- | --- | --- | --- |
| Function Approximation | planned | Replace tables with parameterized value or policy models. | planned |
| DQN | planned | Introduce neural value approximation for discrete actions. | planned |
| Policy Gradient | planned | Optimize parameterized policies directly. | planned |
| Actor-Critic | planned | Combine value estimation and policy optimization. | planned |
| PPO Learnability Check | planned | Test whether a small masked policy can improve on simple baselines. | `rllib_ppo_smoke` is smoke only |
| Action Masking | planned | Prevent invalid UAV service actions during learning. | planned |
| Reward And Training Diagnostics | planned | Inspect reward scale, entropy, policy collapse, and learning instability. | planned |

Track B learns a route from a structured instance:

| Lecture | Status | Purpose | Runnable artifact |
| --- | --- | --- | --- |
| TSP Instance Encoding | planned | Convert the Part I instance into a learning input and permutation mask. | planned |
| TSP Heuristic And Solver References | planned | Reuse Part I route references for held-out learning evaluation. | planned |
| Neural Route Construction | planned | Train and inspect a permutation-producing route policy. | planned |
| Route Execution In GrADyS | planned | Translate ordered stops into simulator actions and compare planned versus executed outcomes. | planned |
| Routing-Only TSP Variants | planned | Change the tour endpoint, travel-cost symmetry, or UAV count one assumption at a time. | planned |

### Part IV: Multi-Agent RL

| Lecture | Status | Purpose | Runnable artifact |
| --- | --- | --- | --- |
| From One UAV To Many UAVs | planned | Identify what changes when the controller becomes multi-agent. | planned |
| PettingZoo Parallel API | planned | Express simultaneous UAV decisions through a standard MARL interface. | `pettingzoo_random` |
| RLlib MultiAgentEnv | planned | Map AeroEdgeRL multi-agent results to RLlib's API contract. | `rllib_random` |
| Independent Policies | planned | Train or evaluate UAV policies independently. | planned |
| Shared-Policy PPO | planned | Use one policy across homogeneous UAV agents. | planned |
| Centralized Critic State | planned | Define global state for centralized training. | planned |
| IPPO And MAPPO-Style Designs | planned | Compare independent and centralized-critic training paths. | planned |

### Part V: Research Experiments

| Lecture | Status | Purpose | Runnable artifact |
| --- | --- | --- | --- |
| Scenario Design | planned | Turn a research idea into a scenario specification. | planned |
| Later Service And Dynamic Extensions | planned | Introduce values, deadlines, arrivals, or replanning only with a revised problem model. | planned |
| Heuristic Baseline Design | planned | Build interpretable non-RL policies before training. | planned |
| Experiment Levels | planned | Separate smoke, sanity, and research experiments. | planned |
| Multi-Seed Evaluation | planned | Report mean, variance, and reproducibility conditions. | planned |
| Windows GPU Training Workflow | planned | Move longer RLlib runs to the WSL2 GPU host. | planned |
| UAV Trajectory Visualization | planned | Use trajectory plots to verify policy behavior and scenario validity. | planned |
| Experiment Reporting | planned | Record commands, configs, metrics, trajectories, and conclusions. | planned |

## Standard Lecture Shape

Each lecture should follow the template defined in
[Course Design](lecture_design.md):

- learning goals;
- problem background;
- theory;
- AeroEdgeRL contract;
- minimal runnable example;
- simulation or training effect;
- common mistakes;
- next step.

This common shape keeps theoretical depth connected to executable experiments.

## Running Examples

Use the `aeroedge-rl` conda environment:

```bash
conda activate aeroedge-rl
cd /Users/wupengfei/Documents/Framework4test/AeroEdgeRL
python scripts/check_environment.py
```

The formal static TSP example has a [scenario contract](../scenarios/static_sensor_tsp.md)
but no runnable CLI yet. The following command runs the earlier dynamic
edge-service **prototype**:

```bash
python -m aeroedge_rl.experiments.cli.no_rl_demo
```

For an interactive RLlib PPO smoke test on that prototype:

```bash
python -m aeroedge_rl.experiments.cli.rllib_ppo_smoke \
  --iterations 1 \
  --num-uavs 1 \
  --num-devices 3 \
  --episode-duration 3 \
  --candidate-limit 2 \
  --train-batch-size 16 \
  --minibatch-size 8 \
  --rollout-fragment-length 4 \
  --num-epochs 1 \
  --quiet \
  --output /tmp/aeroedge_rllib_ppo_smoke_metrics.json
```

This command is a smoke test, not a research result.

## Local Preview

```bash
conda activate aeroedge-rl
cd /Users/wupengfei/Documents/Framework4test/AeroEdgeRL
mkdocs serve
```

Then open the local URL printed by MkDocs.

## External Reference Pattern

The lecture organization borrows the documentation style of GrADyS-SIM NextGen:

- explain simulator purpose before advanced logic;
- introduce execution semantics;
- make nodes, protocols, handlers, and simulation lifecycle visible;
- give a no-RL scenario before RL;
- keep runnable commands next to conceptual explanations.

Useful references:

- [GrADyS-SIM Introduction](https://project-gradys.github.io/gradys-sim-nextgen/)
- [Execution Modes](https://project-gradys.github.io/gradys-sim-nextgen/Getting%20Started/execution/)
- [Simulation Module](https://project-gradys.github.io/gradys-sim-nextgen/Modules/Simulator/simulation/)
- [Timer Handler](https://project-gradys.github.io/gradys-sim-nextgen/Modules/Simulator/handlers/timer/)
- [Data Collection Guide](https://project-gradys.github.io/gradys-sim-nextgen/Guides/2_simple/)
