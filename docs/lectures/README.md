# AeroEdgeRL Lecture Notes

The lecture notes are the guided learning path for AeroEdgeRL.

They are not a generic reinforcement-learning textbook. They teach how to move
from discrete-event UAV simulation to heuristic closed loops and then to
reproducible RL experiments.

## How To Read These Notes

Read the lectures in this order:

```text
simulation first
  -> scenario dynamics
  -> heuristic baseline
  -> RL formulation
  -> RL algorithm
  -> experiment and visualization
```

Do not start from PPO or RLlib. In AeroEdgeRL, an RL result is meaningful only
after the underlying scenario can be explained without RL.

## Course Map

| Part | Theme | Goal |
| --- | --- | --- |
| I | Simulation First | Understand the preserved GrADyS-SIM discrete-event core and run a UAV scenario without RL. |
| II | RL Foundations | Map simulator outputs to MDP concepts and reproduce tabular RL algorithms. |
| III | Deep RL | Move from tabular algorithms to practical deep RL with reproducible smoke experiments. |
| IV | Multi-Agent RL | Extend from one controller to multi-UAV learning. |
| V | Research Experiments | Turn a scenario and an algorithm into a research-grade experiment. |

### Part I: Simulation First

| Lecture | Status | Purpose | Runnable artifact |
| --- | --- | --- | --- |
| [Course Design](lecture_design.md) | current | Define the structure and teaching contract of the lecture series. | MkDocs preview |
| [Simulation-First Roadmap](00_simulation_first_roadmap.md) | current | Explain why AeroEdgeRL starts from simulation rather than RL training. | `scripts/check_environment.py` |
| [GrADyS Core In AeroEdgeRL](01_gradys_core_in_aeroedge.md) | current | Explain discrete-event simulation, handlers, protocols, and the AeroEdgeRL boundary. | `python -m aeroedge_rl.experiments.cli.no_rl_demo` |
| [No-RL UAV Edge Service Demo](02_no_rl_uav_edge_demo.md) | current | Run and interpret the first UAV edge-service scenario without RL. | `no_rl_demo`; `baselines` |
| [Heuristic Closed Loop](03_heuristic_closed_loop.md) | current | Compare rules, inputs, and measured outcomes in a complete simulator loop. | `no_rl_demo`; `baselines` |
| [Trajectory Data And Visualization](04_trajectory_data_and_visualization.md) | current | Inspect decisions, metrics, and UAV paths in one complete non-RL example. | `no_rl_demo --plot-output`; `baselines` |
| Simulator Time Versus Wall-Clock Time | planned | Separate discrete-event simulated time from training runtime and logging time. | planned |

### Part II: RL Foundations

| Lecture | Status | Purpose | Runnable artifact |
| --- | --- | --- | --- |
| MDP Formulation | planned | Map UAV edge-service simulation to state, action, reward, transition, and discount factor. | planned |
| Return And Value Functions | planned | Define return, state value, and action value in simulator-facing terms. | planned |
| Bellman Equations | planned | Derive Bellman expectation and optimality equations for the scenario. | planned |
| Dynamic Programming | planned | Reproduce policy evaluation and policy improvement in a small controlled setting. | planned |
| Monte Carlo Methods | planned | Estimate returns from sampled episodes. | planned |
| Temporal-Difference Learning | planned | Learn from partial episode transitions. | planned |
| SARSA | planned | Compare on-policy TD control with simulator-generated trajectories. | planned |
| Q-learning | planned | Compare off-policy TD control with heuristic baselines. | planned |

### Part III: Deep RL

| Lecture | Status | Purpose | Runnable artifact |
| --- | --- | --- | --- |
| Function Approximation | planned | Replace tables with parameterized value or policy models. | planned |
| DQN | planned | Introduce neural value approximation for discrete actions. | planned |
| Policy Gradient | planned | Optimize parameterized policies directly. | planned |
| Actor-Critic | planned | Combine value estimation and policy optimization. | planned |
| PPO | planned | Use PPO as the first practical deep RL training target. | `rllib_ppo_smoke` |
| Action Masking | planned | Prevent invalid UAV service actions during learning. | planned |
| Reward And Training Diagnostics | planned | Inspect reward scale, entropy, policy collapse, and learning instability. | planned |

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

Then run the current no-RL demo:

```bash
python -m aeroedge_rl.experiments.cli.no_rl_demo
```

For RLlib PPO smoke testing:

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
