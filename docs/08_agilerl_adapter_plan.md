# AgileRL Adapter Plan

## Decision

AgileRL should use a separate Python 3.11 conda environment:

```text
aeroedge-rl       -> Python 3.10, RLlib/Gymnasium/PettingZoo PPO development
aeroedge-agilerl  -> Python 3.11, AgileRL experiments
```

This split is intentional. On the Mac environment validated on 2026-07-13:

- Ray/RLlib 2.49.2 requires Gymnasium 1.x APIs such as `VectorizeMode`.
- PyTorch 2.2.2 on macOS x86_64 requires `numpy<2` for NumPy interop.
- AgileRL 1.0.13 requires `gymnasium<0.30.0`, which breaks RLlib 2.49.2.
- AgileRL 2.7.1 requires dependencies that are not available for Python 3.10.

Trying to force all training libraries into one Python 3.10 environment makes
the environment unstable. AeroEdgeRL therefore treats AgileRL as a separate
training backend environment, not as part of the default RLlib development env.

## Setup

From the AeroEdgeRL repository:

```bash
conda env create -f environment-agilerl.yml
conda activate aeroedge-agilerl
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ../gradys-sim-nextgen --no-deps --no-build-isolation
python -m pip install -e . --no-deps --no-build-isolation
python scripts/check_environment.py
```

## Adapter Strategy

AgileRL should consume AeroEdgeRL through already-standard interfaces first:

```text
AeroEdgeRL core scenario
  -> Gymnasium adapter for single-policy experiments
  -> PettingZoo parallel adapter for multi-agent experiments
  -> AgileRL experiment runner
```

Do not fork the simulator dynamics for AgileRL. The GrADyS discrete-event core,
scenario reset/step lifecycle, action masks, rewards, and metrics must remain
owned by the existing core scenario and adapters.

## Phase 1 Scope

The first AgileRL integration should be a smoke-level runner:

- import AgileRL in `aeroedge-agilerl`;
- instantiate the existing Gymnasium or PettingZoo adapter;
- run one tiny training or rollout loop;
- write a compact JSON metrics file under `outputs/`;
- document exact package versions and command line.

Only after the smoke runner is stable should we add algorithm-specific training
presets, checkpoint evaluation, or multi-seed sweeps.
