# Phase 1 Migration Design

## Goal

Phase 1 turns the existing `showcases/rl-bridge` prototype into the first
formal AeroEdgeRL package.

The migration should be conservative. The goal is not to redesign every model
at once. The goal is to move the working closed loop into a maintainable package
while preserving the GrADyS-SIM discrete-event simulation core.

## Source Prototype

Current source:

```text
/Users/wupengfei/Documents/Framework4test/gradys-sim-nextgen/showcases/rl-bridge
```

The prototype already has the correct architectural direction:

```text
GrADyS simulator
  -> dependency-light core environment
  -> Gymnasium adapter
  -> PettingZoo adapter
  -> RLlib adapter
  -> training and evaluation scripts
```

Phase 1 should formalize that direction and remove showcase-specific coupling.

## Migration Principle

Keep the simulator as simulator.

Do not move Gymnasium, PettingZoo, RLlib, AgileRL, Ray, Torch, or training
logic into the simulation kernel. The RL layer wraps simulator behavior; it does
not redefine simulated time, event scheduling, node lifecycle, communication, or
mobility.

## Target Package Skeleton

```text
aeroedge_rl/
  __init__.py

  rl/
    __init__.py
    core_env.py
    result.py
    masks.py
    spaces.py

  scenarios/
    __init__.py
    uav_edge_service/
      __init__.py
      config.py
      environment.py
      protocols.py
      tasks.py
      workload.py
      observations.py
      rewards.py
      actions.py
      metrics.py

  adapters/
    __init__.py
    gymnasium_env.py
    pettingzoo_parallel_env.py
    rllib_multiagent_env.py
    rllib_action_mask_model.py

  baselines/
    __init__.py
    policies.py

  experiments/
    __init__.py
    runner.py
    cli/
      random_rollout.py
      baselines.py
      rllib_ppo_smoke.py
      rllib_ppo_train.py
```

## File Migration Map

| Current file | Target | Phase 1 treatment |
| --- | --- | --- |
| `gradys_uav_service_env.py` | `scenarios/uav_edge_service/environment.py` | Split into config, task, environment, observations, rewards, actions, metrics. |
| `rl_protocols.py` | `scenarios/uav_edge_service/protocols.py` | Keep minimal external-control protocols. |
| `workload.py` | `scenarios/uav_edge_service/workload.py` | Keep synthetic and Alibaba-derived workload support. |
| `gymnasium_adapter.py` | `adapters/gymnasium_env.py` | Keep optional Gymnasium import path. |
| `pettingzoo_parallel_adapter.py` | `adapters/pettingzoo_parallel_env.py` | Keep as main MARL standard adapter. |
| `rllib_multiagent_adapter.py` | `adapters/rllib_multiagent_env.py` | Keep but remove private-field access. |
| `rllib_action_mask_model.py` | `adapters/rllib_action_mask_model.py` | Keep as optional old-stack RLlib model. |
| `baseline_policies.py` | `baselines/policies.py` | Keep random, nearest, EDF, SLO-risk. |
| `experiment_runner.py` | `experiments/runner.py` | Keep common episode runner and CSV summary. |
| `main_random.py` | `experiments/cli/random_rollout.py` | Convert to module CLI. |
| `main_baselines.py` | `experiments/cli/baselines.py` | Convert to module CLI. |
| `main_gym_random.py` | `experiments/cli/gym_random.py` | Keep as smoke test CLI if useful. |
| `main_rllib_random.py` | `experiments/cli/rllib_random.py` | Keep as smoke test CLI. |
| `main_rllib_ppo_smoke.py` | `experiments/cli/rllib_ppo_smoke.py` | Keep as fast training sanity check. |
| `main_rllib_ppo_train.py` | `experiments/cli/rllib_ppo_train.py` | Keep as reproducible training entry. |
| `main_visualize.py` | `experiments/cli/visualize.py` | Keep after visualization API stabilizes. |
| `PPO_RESULTS.md` | `references/results/` | Preserve as historical result. |
| `CLOSED_LOOP_GUIDE.md` | `docs/` or `references/` | Convert into formal architecture docs. |
| `ENVIRONMENT.md` | `docs/` | Convert into install and environment docs. |

## Public Core APIs To Stabilize

The first package version should expose these backend-independent APIs:

```python
env.reset(seed=None) -> dict[AgentId, Observation]
env.step(actions: dict[AgentId, Action]) -> StepResult
env.close() -> None
env.render_text() -> str
env.metrics_snapshot() -> dict[str, float]
env.visualization_snapshot() -> dict[str, object]
env.action_mask(agent_id: str) -> list[float]
env.global_state() -> list[float]
env.agent_position(agent_id: str) -> tuple[float, float, float]
env.candidate_tasks(agent_id: str) -> list[Task]
```

`StepResult` should become a small shared dataclass:

```python
@dataclass
class StepResult:
    observations: dict[str, Observation]
    rewards: dict[str, float]
    terminated: bool
    truncated: bool
    infos: dict[str, dict]
```

## Adapter Rules

Adapters must not read private scenario fields such as `_busy_until`,
`_targets`, `_tasks`, or `_simulation`.

Instead:

- action masks come from `env.action_mask(agent_id)`;
- global critic state comes from `env.global_state()`;
- observations come from `StepResult.observations`;
- metrics come from `env.metrics_snapshot()`;
- visualization comes from `env.visualization_snapshot()`.

This keeps RLlib, PettingZoo, Gymnasium, and AgileRL behavior outside the
scenario internals.

## Package Dependency Rules

Core package:

```text
aeroedge_rl.rl
aeroedge_rl.scenarios
aeroedge_rl.baselines
aeroedge_rl.experiments.runner
```

should require only lightweight dependencies already needed by the simulator
and data utilities.

Optional adapter dependencies:

```text
aeroedge_rl.adapters.gymnasium_env
  -> gymnasium, numpy

aeroedge_rl.adapters.pettingzoo_parallel_env
  -> gymnasium, pettingzoo, numpy

aeroedge_rl.adapters.rllib_multiagent_env
  -> gymnasium, ray[rllib], numpy

aeroedge_rl.adapters.rllib_action_mask_model
  -> ray[rllib], torch
```

## Phase 1 Task Breakdown

### Step 1: Create Package Scaffold

Create package folders, `pyproject.toml`, and minimal imports. Keep the package
name `aeroedge_rl`.

### Step 2: Move Core Environment

Move the current GrADyS-backed core environment into the scenario package.
During this step, keep behavior equivalent to the prototype.

### Step 3: Split Large Environment File

Separate:

- config;
- task model;
- workload;
- action decoding;
- observation builder;
- reward logic;
- metrics;
- protocols.

This should be a mechanical split first, not a conceptual rewrite.

### Step 4: Add Public Mask and State APIs

Implement:

```python
action_mask(agent_id)
global_state()
```

Then modify RLlib adapter so it stops reading private fields.

### Step 5: Move Adapters

Move Gymnasium, PettingZoo, and RLlib wrappers into `adapters/`. Keep imports
optional and fail with clear `ImportError` messages when extras are missing.

### Step 6: Move Baselines and Runner

Move baseline policies and reusable episode runner. Convert scripts into
module CLIs.

### Step 7: Add Tests

Minimum tests:

- `test_core_reset.py`
- `test_core_step.py`
- `test_action_mask.py`
- `test_seed_reproducibility.py`
- `test_gymnasium_adapter.py`
- `test_pettingzoo_adapter.py`
- `test_rllib_adapter_contract.py`

Adapter tests should skip cleanly when optional dependencies are not installed.

## Acceptance Criteria

Phase 1 is complete when:

- `python -m aeroedge_rl.experiments.cli.random_rollout` runs.
- `python -m aeroedge_rl.experiments.cli.baselines` runs.
- Gymnasium random rollout runs if `gymnasium` is installed.
- PettingZoo random rollout runs if `pettingzoo` is installed.
- RLlib random rollout runs if `ray[rllib]` is installed.
- No adapter reads private fields from the core environment.
- Tests prove reset, step, action mask, and seed reproducibility.

## Non-Goals

Phase 1 should not:

- redesign the reward function;
- introduce a new UAV physics model;
- add MAPPO from scratch;
- optimize training performance;
- replace GrADyS event scheduling;
- integrate AgileRL beyond documenting the PettingZoo/Gymnasium path.

## Open Design Questions

1. Should AeroEdgeRL vendor a copy of the GrADyS simulator core, or depend on a
   local/imported `gradysim` package first?
2. Should `advance_until(target_time)` be added to GrADyS-SIM directly before
   migrating the RL bridge?
3. Should scenario configs use plain dataclasses first or move immediately to
   Pydantic/Hydra/OmegaConf?
4. Should outputs use CSV/JSON only in Phase 1, or should TensorBoard/W&B be
   introduced later?

## Recommended Decision For Phase 1

Use the existing local GrADyS-SIM package as the simulator dependency during
Phase 1. Do not vendor the simulator yet.

Reason:

- It keeps the migration small.
- It preserves the original event-driven behavior.
- It lets AeroEdgeRL stabilize its RL abstractions before deciding whether to
  fork, vendor, or upstream simulator changes.

