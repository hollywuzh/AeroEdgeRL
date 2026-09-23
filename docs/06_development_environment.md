# Development Environment

## Decision

AeroEdgeRL should use a clean project-specific conda environment.

Do not rely on `PYTHONPATH` as the normal development workflow. `PYTHONPATH`
is acceptable for temporary smoke tests, but the reliable long-term approach is
to install both local workspaces into one isolated environment in editable mode:

```text
gradys-sim-nextgen  -> editable install, provides local `gradysim`
AeroEdgeRL          -> editable install, provides local `aeroedge_rl`
```

This removes the ambiguity where Python may accidentally import an older
site-packages version of `gradysim`.

## Recommended Mac Development Environment

From any terminal:

```bash
conda env create -f environment.yml
conda activate aeroedge-rl
python -m pip install --upgrade pip setuptools wheel
```

If `conda env create` is slow while solving conda-forge metadata, use this
fallback and then install the base pip dependencies explicitly:

```bash
conda create -n aeroedge-rl python=3.10 pip cryptography -y
conda activate aeroedge-rl
python -m pip install --upgrade pip setuptools wheel
python -m pip install "websockets>=12" "pandas>=2.2.3" "aiohttp>=3.11.14" "gymnasium==1.1.1" "numpy<2" "pettingzoo==1.26.1" "ray[rllib]" torch pytest ruff
```

Install the local GrADyS-SIM workspace first:

```bash
python -m pip install -e /Users/wupengfei/Documents/Framework4test/gradys-sim-nextgen --no-deps --no-build-isolation
```

Install AeroEdgeRL second:

```bash
python -m pip install -e /Users/wupengfei/Documents/Framework4test/AeroEdgeRL --no-deps --no-build-isolation
```

Then verify:

```bash
cd /Users/wupengfei/Documents/Framework4test/AeroEdgeRL
python scripts/check_environment.py
pytest -q -p no:cacheprovider
python -m aeroedge_rl.experiments.cli.random_rollout
python -m aeroedge_rl.experiments.cli.gym_random
python -m aeroedge_rl.experiments.cli.pettingzoo_random
```

After editable installs, these commands should not require `PYTHONPATH`.

### Optional Mac Training Layer

The Mac can also smoke-test the RLlib training adapter, but long training
should still happen on the Windows/WSL2 GPU machine.

When using the fallback setup, install RLlib training libraries in layers so
dependency resolver behavior is visible:

```bash
python -m pip install "ray[rllib]"
python -m pip install torch
python -m pip install "numpy<2"
```

On the Mac environment validated on 2026-07-13, the important RLlib training
packages are:

```text
ray        2.49.2
torch      2.2.2
gymnasium  1.1.1
pettingzoo 1.26.1
numpy      1.26.4  # keep numpy<2 for torch 2.2.x on macOS x86_64
```

After installing this layer, rerun:

```bash
pytest -q -rs -p no:cacheprovider
python -m aeroedge_rl.experiments.cli.rllib_random --output /tmp/aeroedge_rllib_random_rollout.jsonl
python -m aeroedge_rl.experiments.cli.rllib_ppo_smoke --iterations 1 --num-uavs 1 --num-devices 3 --episode-duration 3 --candidate-limit 2 --train-batch-size 16 --minibatch-size 8 --rollout-fragment-length 4 --num-epochs 1 --quiet --output /tmp/aeroedge_rllib_ppo_smoke_metrics.json
```

### AgileRL Environment

Do not install AgileRL into `aeroedge-rl` on Python 3.10. AgileRL 1.0.13 forces
`gymnasium<0.30.0`, which breaks RLlib 2.49.2. AgileRL 2.7.1 requires a Python
3.11-compatible dependency set.

Use a separate environment:

```bash
conda env create -f environment-agilerl.yml
conda activate aeroedge-agilerl
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e /Users/wupengfei/Documents/Framework4test/gradys-sim-nextgen --no-deps --no-build-isolation
python -m pip install -e /Users/wupengfei/Documents/Framework4test/AeroEdgeRL --no-deps --no-build-isolation
python scripts/check_environment.py
```

The AgileRL integration plan is tracked in
[AgileRL Adapter Plan](08_agilerl_adapter_plan.md).

### ArduPilot/UAV API Dependency

The GrADyS-SIM package declares `uav-api>=0.1.3`, which is used by the
ArduPilot mobility handler. AeroEdgeRL Phase 1 does not require this path for
the preserved discrete-event core, timer handler, dynamic velocity mobility, or
RL adapters.

On the Mac environment validated on 2026-07-12, installing `uav-api` attempted
to build `fastcrc` through Rust/crates.io and failed because the local proxy
target `127.0.0.1:7890` was unreachable. Therefore `pip check` may report:

```text
gradysim 0.8.0 requires uav-api, which is not installed.
```

Treat this as an ArduPilot optional-integration gap, not as a blocker for the
core AeroEdgeRL development environment. Resolve it only when working on
ArduPilot/SITL integration.

## Recommended Windows GPU Environment

Use Windows as the host OS, but do RL training inside WSL2 Ubuntu.

Inside WSL2:

```bash
conda env create -f environment.yml
conda activate aeroedge-rl
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e /path/to/gradys-sim-nextgen --no-deps --no-build-isolation
python -m pip install -e /path/to/AeroEdgeRL --no-deps --no-build-isolation
python -m pip install "ray[rllib]" torch "numpy<2"
```

For AgileRL experiments:

```bash
conda env create -f environment-agilerl.yml
conda activate aeroedge-agilerl
```

For full training machines, keep outputs and checkpoints outside git:

```text
outputs/
checkpoints/
```

These paths are already ignored by `.gitignore`.

## Why Not Use Only `PYTHONPATH`?

`PYTHONPATH` works for quick checks, but it is fragile:

- terminal sessions can forget it;
- IDEs may not inherit it;
- notebooks often use a different kernel;
- Ray/RLlib workers may spawn subprocesses with a different environment;
- path ordering can accidentally prefer site-packages over the local workspace.

Editable installs solve this by registering the local source trees in the active
environment.

## Required Import Invariant

During Phase 1, AeroEdgeRL expects:

```text
import gradysim
```

to resolve to:

```text
/Users/wupengfei/Documents/Framework4test/gradys-sim-nextgen/gradysim
```

on the Mac development machine.

The environment check script verifies this. If the workspaces are not siblings
or are located somewhere else, set:

```bash
export AEROEDGE_GRADYSIM_ROOT=/absolute/path/to/gradys-sim-nextgen
```

before running:

```bash
python scripts/check_environment.py
```

## Practical Rule

Use:

```text
conda env + editable installs
```

as the normal workflow.

Use:

```text
PYTHONPATH
```

only for one-off rescue checks before the environment is installed.

## Multi-Host Workflow

The full Mac plus WSL2 GPU workflow is documented in
[Multi-Host Development Model](07_multi_host_development_model.md).
