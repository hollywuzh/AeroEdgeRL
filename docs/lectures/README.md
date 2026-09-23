# AeroEdgeRL Lecture Notes

This folder is the teaching track for AeroEdgeRL.

The lectures are intentionally simulation-first. RL algorithms are introduced
only after the simulator, scenario lifecycle, rule-based policies, metrics, and
experiment artifacts are clear.

The source format is Markdown with LaTeX math. Inline equations use
`\( ... \)`, and display equations use `\[ ... \]`. The MkDocs site renders
these expressions through MathJax.

## External Reference Pattern

The structure borrows from the GrADyS-SIM NextGen documentation:

- start with the simulator's purpose and execution modes;
- explain nodes, protocols, handlers, and simulation building;
- give a complete no-RL scenario before adding advanced logic;
- keep runnable commands next to conceptual explanations.

Useful source pages:

- [GrADyS-SIM Introduction](https://project-gradys.github.io/gradys-sim-nextgen/)
- [Execution Modes](https://project-gradys.github.io/gradys-sim-nextgen/Getting%20Started/execution/)
- [Simulation Module](https://project-gradys.github.io/gradys-sim-nextgen/Modules/Simulator/simulation/)
- [Timer Handler](https://project-gradys.github.io/gradys-sim-nextgen/Modules/Simulator/handlers/timer/)
- [Data Collection Guide](https://project-gradys.github.io/gradys-sim-nextgen/Guides/2_simple/)

## Lecture Sequence

| Part | Lecture | Goal | Runnable artifact |
| --- | --- | --- | --- |
| 0 | [Simulation-First Roadmap](00_simulation_first_roadmap.md) | Establish the teaching contract and simulator-first order. | `scripts/check_environment.py` |
| 1 | [GrADyS Core In AeroEdgeRL](01_gradys_core_in_aeroedge.md) | Explain discrete-event simulation, protocols, handlers, and the AeroEdgeRL scenario wrapper. | `python -m aeroedge_rl.experiments.cli.no_rl_demo` |
| 2 | [No-RL UAV Edge Service Demo](02_no_rl_uav_edge_demo.md) | Run and interpret rule-based UAV task selection policies. | `no_rl_demo`, `baselines` |
| 3 | Tabular Q-learning | Add the first learning algorithm after the no-RL baseline is measurable. | planned |
| 4 | SARSA vs Q-learning | Compare on-policy and off-policy TD control. | planned |
| 5 | DQN | Replace the table with a neural value approximator. | planned |
| 6 | PPO With RLlib | Use the existing RLlib PPO smoke as the first policy-gradient backend. | `rllib_ppo_smoke` |
| 7 | Shared-Policy MARL | Move from one UAV to many UAVs with shared policy and action masks. | planned |

## Standard Lecture Template

Each lecture should use this shape:

```text
1. Motivation
2. System model
3. Inputs and outputs
4. Simulator lifecycle
5. Policy or algorithm
6. Runnable command
7. Expected output
8. Metrics to inspect
9. What can go wrong
10. Bridge to the next lecture
```

The lecture artifacts should remain executable. A reader should be able to copy
the command, run it in `aeroedge-rl`, and see the same category of result.

## Local Preview

```bash
conda activate aeroedge-rl
cd /Users/wupengfei/Documents/Framework4test/AeroEdgeRL
mkdocs serve
```
