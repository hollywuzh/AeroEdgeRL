# Phase 1 Implementation Plan

## Purpose

This document turns the Phase 1 migration design into an executable task plan.

Phase 1 has one practical goal:

> Move the working `showcases/rl-bridge` prototype into a formal
> `aeroedge_rl` package without breaking the GrADyS-SIM discrete-event
> simulation loop.

The work should proceed in small, testable steps. Each step should preserve a
running random rollout before moving on.

## Ground Rules

1. Do not rewrite the simulator core during Phase 1.
2. Do not vendor GrADyS-SIM into AeroEdgeRL yet.
3. Do not make Gymnasium, PettingZoo, RLlib, AgileRL, Ray, or Torch required
   dependencies of the core package.
4. Keep behavior equivalent to the current `rl-bridge` prototype before doing
   architectural cleanup.
5. Replace private-field adapter access with public core APIs before declaring
   Phase 1 complete.
6. Use a clean conda environment with editable installs for both
   `gradys-sim-nextgen` and `AeroEdgeRL`; do not rely on `PYTHONPATH` as the
   normal development workflow.
7. Treat Mac as the primary development host and WSL2 on the Windows GPU
   machine as the primary training host.

## Working Source And Target

Source prototype:

```text
/Users/wupengfei/Documents/Framework4test/gradys-sim-nextgen/showcases/rl-bridge
```

Target project:

```text
/Users/wupengfei/Documents/Framework4test/AeroEdgeRL
```

Target package:

```text
aeroedge_rl
```

## Step 0: Create Git And Package Baseline

Tasks:

- Initialize a git repository for AeroEdgeRL if one does not already exist.
- Add `.gitignore`.
- Add `pyproject.toml`.
- Add `README.md`, `docs/`, `design/`, `roadmap/`, `references/`.
- Add empty package skeleton under `aeroedge_rl/`.
- Add empty `tests/`.

Initial package tree:

```text
aeroedge_rl/
  __init__.py
  rl/__init__.py
  scenarios/__init__.py
  scenarios/uav_edge_service/__init__.py
  adapters/__init__.py
  baselines/__init__.py
  experiments/__init__.py
  experiments/cli/__init__.py
tests/
```

Validation:

```bash
python -m pip install -e .
python -c "import aeroedge_rl; print(aeroedge_rl.__version__)"
python scripts/check_environment.py
```

Exit criteria:

- The package imports locally.
- No RL optional dependency is imported during `import aeroedge_rl`.
- `gradysim` resolves to the expected local GrADyS-SIM workspace.
- The multi-host setup rules are recorded for GitHub users.

## Step 1: Move The Prototype As-Is

Tasks:

- Copy the minimal working RL bridge files into package locations.
- Prefer mechanical moves over refactors.
- Keep old behavior passing before splitting files.

Initial move:

```text
gradys_uav_service_env.py
  -> aeroedge_rl/scenarios/uav_edge_service/environment.py

rl_protocols.py
  -> aeroedge_rl/scenarios/uav_edge_service/protocols.py

workload.py
  -> aeroedge_rl/scenarios/uav_edge_service/workload.py

baseline_policies.py
  -> aeroedge_rl/baselines/policies.py

experiment_runner.py
  -> aeroedge_rl/experiments/runner.py
```

Temporary compatibility rule:

- It is acceptable for `environment.py` to remain large during Step 1.
- It is acceptable for import paths to be adjusted minimally.

Validation:

```bash
python -m aeroedge_rl.experiments.cli.random_rollout
```

Exit criteria:

- A random rollout runs with the same behavior as the showcase prototype.

## Step 2: Add Core Result And Public APIs

Tasks:

- Move `StepResult` into `aeroedge_rl/rl/result.py`.
- Define public type aliases in `aeroedge_rl/rl/core_env.py` or
  `aeroedge_rl/rl/types.py`.
- Add public methods to the UAV edge-service environment:

```python
action_mask(agent_id: str)
global_state()
agent_position(agent_id: str)
metrics_snapshot()
visualization_snapshot()
candidate_tasks(agent_id: str)
```

Required behavior:

- `action_mask(agent_id)` must encode valid hover/task-choice actions.
- `global_state()` must return a stable vector or documented placeholder.
- Existing observations and rewards must remain unchanged.

Validation:

```bash
pytest tests/test_core_reset.py tests/test_core_step.py tests/test_action_mask.py -q
```

Exit criteria:

- Core environment no longer requires adapter code to inspect private fields.

## Step 3: Move Gymnasium Adapter

Tasks:

- Move `gymnasium_adapter.py` to `aeroedge_rl/adapters/gymnasium_env.py`.
- Keep Gymnasium as an optional import.
- Raise a clear `ImportError` if Gymnasium is missing.
- Add a random Gymnasium rollout CLI.

Validation:

```bash
python -m aeroedge_rl.experiments.cli.gym_random
pytest tests/test_gymnasium_adapter.py -q
```

Skip rule:

- Tests should skip if Gymnasium is not installed.

Exit criteria:

- Centralized Gymnasium random rollout works.

## Step 4: Move PettingZoo Adapter

Tasks:

- Move `pettingzoo_parallel_adapter.py` to
  `aeroedge_rl/adapters/pettingzoo_parallel_env.py`.
- Keep PettingZoo as an optional import.
- Ensure `possible_agents`, `agents`, `observation_space(agent)`, and
  `action_space(agent)` behave consistently.

Validation:

```bash
python -m aeroedge_rl.experiments.cli.pettingzoo_random
pytest tests/test_pettingzoo_adapter.py -q
```

Skip rule:

- Tests should skip if PettingZoo is not installed.

Exit criteria:

- Parallel multi-agent random rollout works.

## Step 5: Move RLlib Adapter

Tasks:

- Move `rllib_multiagent_adapter.py` to
  `aeroedge_rl/adapters/rllib_multiagent_env.py`.
- Move `rllib_action_mask_model.py` to
  `aeroedge_rl/adapters/rllib_action_mask_model.py`.
- Replace private field reads with:

```python
self.core.action_mask(agent)
```

- Keep RLlib and Torch imports optional.

Validation:

```bash
python -m aeroedge_rl.experiments.cli.rllib_random
pytest tests/test_rllib_adapter_contract.py -q
```

Skip rule:

- Tests should skip if RLlib is not installed.

Exit criteria:

- RLlib random rollout works.
- RLlib adapter does not access private environment fields.

## Step 6: Convert Scripts To Module CLIs

Tasks:

- Convert runnable scripts into `aeroedge_rl.experiments.cli`.
- Keep CLI names clear and minimal.

Target commands:

```bash
python -m aeroedge_rl.experiments.cli.random_rollout
python -m aeroedge_rl.experiments.cli.baselines
python -m aeroedge_rl.experiments.cli.gym_random
python -m aeroedge_rl.experiments.cli.pettingzoo_random
python -m aeroedge_rl.experiments.cli.rllib_random
python -m aeroedge_rl.experiments.cli.rllib_ppo_smoke
python -m aeroedge_rl.experiments.cli.rllib_ppo_train
```

Exit criteria:

- CLI entry points run from the project root after editable install.

## Step 7: Split The Environment File

Tasks:

Split the large environment module into:

```text
config.py
tasks.py
workload.py
protocols.py
actions.py
observations.py
rewards.py
metrics.py
environment.py
```

Guideline:

- Split mechanically first.
- Preserve behavior.
- Avoid redesigning reward and task semantics in this phase.

Validation:

```bash
pytest tests/test_core_reset.py tests/test_core_step.py tests/test_seed_reproducibility.py -q
python -m aeroedge_rl.experiments.cli.random_rollout
```

Exit criteria:

- The package is easier to navigate.
- Behavior remains equivalent to the pre-split version.

## Step 8: Add Reproducibility Tests

Tasks:

- Test that same seed gives same initial device positions and tasks.
- Test that same action sequence gives same metrics.
- Test that different seeds alter generated workload or positions.

Minimum tests:

```text
tests/test_seed_reproducibility.py
tests/test_metrics_snapshot.py
tests/test_action_mask.py
```

Exit criteria:

- Reproducibility behavior is documented and tested.

## Step 9: Preserve Historical Results

Tasks:

- Move current prototype notes into `references/`.
- Preserve `PPO_RESULTS.md` as a historical benchmark note.
- Record the exact command used for the current PPO milestone.

Target:

```text
references/results/ppo_results_from_rl_bridge.md
references/prototype/closed_loop_guide.md
references/prototype/environment_notes.md
```

Exit criteria:

- Old results are available, but not mixed with package source.

## Step 10: Phase 1 Review

Review checklist:

- Core package imports without optional RL libraries.
- GrADyS-SIM remains the simulation backend.
- Random rollout runs.
- Baselines run.
- Gymnasium adapter runs when installed.
- PettingZoo adapter runs when installed.
- RLlib adapter runs when installed.
- Action masks are public API-based.
- Tests cover reset, step, seed, masks, and adapter contracts.
- Documentation matches implementation.

Phase 1 is complete only when all required checklist items pass.

## Suggested Commit Sequence

1. `docs: add AeroEdgeRL phase 1 implementation plan`
2. `chore: initialize aeroedge_rl package scaffold`
3. `feat: migrate UAV edge service core environment`
4. `feat: add public action mask and global state APIs`
5. `feat: add Gymnasium and PettingZoo adapters`
6. `feat: add RLlib adapter and action mask model`
7. `feat: migrate baselines and experiment runner`
8. `test: add core environment and reproducibility tests`
9. `docs: preserve prototype results and update migration notes`

## Risk Register

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Importing installed `gradysim` instead of local code | Tests may pass or fail against the wrong simulator | Use editable installs and inspect `gradysim.__file__` in dev notes. |
| Optional RL dependencies pollute core imports | Core package becomes heavy and fragile | Keep adapters lazy and optional. |
| Adapter behavior depends on private fields | Refactors break RLlib/Gym wrappers | Add public mask/state APIs and tests. |
| Mechanical split changes behavior | Results become hard to compare | Run random rollout and seed tests after every split. |
| RL control interval semantics remain unclear | Training results become confusing | Defer exact simulator API work to Phase 2, but document current behavior. |

## Stop Conditions

Stop and revise the plan if:

- moving code requires changing GrADyS event-loop semantics;
- optional RL dependencies become mandatory for core import;
- random rollout diverges unexpectedly after a mechanical migration;
- adapter tests require private field access to pass;
- package naming conflicts with installed `gradysim` cannot be controlled.
