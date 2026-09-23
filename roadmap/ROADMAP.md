# Roadmap

## Phase 0: Documentation Foundation

Goal: make the project controllable before adding code.

Tasks:

- Fix project name and positioning.
- Record the GrADyS discrete-event preservation requirement.
- Define architecture layers.
- Define RL adapter strategy.
- Define first benchmark scenario.

Exit criteria:

- The documentation explains what is preserved, what is rewritten, and why.

## Phase 1: Extract Current RL Bridge

Goal: turn the existing `showcases/rl-bridge` prototype into a real package.

Design document:

- [Phase 1 Migration Design](../docs/04_phase1_migration_design.md)
- [Phase 1 Implementation Plan](../docs/05_phase1_implementation_plan.md)

Tasks:

- Move the current core environment into `aeroedge_rl.rl`.
- Move Gymnasium, PettingZoo, and RLlib wrappers into `aeroedge_rl.adapters`.
- Replace private-field access with public environment APIs.
- Add tests for reset, step, action masks, deterministic seeding, and episode
  termination.

Exit criteria:

- A random policy can run through all adapters.

## Phase 2: Stabilize Simulator Control Boundary

Goal: make event-driven simulation and RL control intervals behave cleanly.

Tasks:

- Add official `advance_until(target_time)` behavior.
- Decide whether control intervals are exact, event-aligned, or bounded by
  next-event timestamps.
- Add snapshot APIs for node state, mobility state, and metrics.
- Add seed plumbing for all stochastic components.

Exit criteria:

- Tests prove that one RL step advances the discrete-event simulator in a
  predictable, documented way.

## Phase 3: First Benchmark Scenario

Goal: define a publishable UAV edge-service benchmark.

Tasks:

- Implement UAV-assisted edge service orchestration.
- Add synthetic and trace-driven workloads.
- Add reward presets for throughput, SLO, energy, and fairness.
- Add baselines: random, nearest, EDF, SLO-risk, patrol.
- Add visualization and CSV/JSON metrics.

Exit criteria:

- A reproducible experiment compares baselines with PPO/IPPO.

## Phase 4: Multi-Agent Training

Goal: make MARL experiments first-class.

Tasks:

- RLlib shared-policy PPO/IPPO.
- PettingZoo-compatible AgileRL experiments.
- Action masking.
- Centralized critic state.
- Scenario registry and experiment registry.

Exit criteria:

- A multi-agent training run can be reproduced from one config file.

## Phase 5: Research Expansion

Candidate directions:

- UAV swarm service orchestration.
- Post-disaster edge intelligence.
- Low-altitude sensing-communication-computation integration.
- Network security and adversarial routing.
- SLO-aware trajectory and resource co-optimization.
- Training-inference separation for UAV edge intelligence.
