# Project Context Handoff

This document records the current design context of AeroEdgeRL so that the
project can be resumed on another host, especially the Windows GPU machine.

## Project Identity

AeroEdgeRL is an RL-first UAV edge intelligence simulation framework.

The project does not replace GrADyS-SIM. Its core architectural decision is:

> Preserve the GrADyS-SIM discrete-event simulation core, and build RL-facing
> abstractions and adapters around it.

GrADyS-SIM owns simulated time, event scheduling, node lifecycle, communication,
mobility, telemetry, and scenario dynamics. AeroEdgeRL owns observations,
actions, rewards, masks, metrics, experiment entry points, and integration with
mainstream RL libraries.

## Design Boundary

The intended dependency boundary is:

```text
sim / scenario core
  must not import Gymnasium, PettingZoo, RLlib, AgileRL, Ray, Torch, or JAX

rl
  may define backend-independent RL concepts

adapters
  may import optional RL libraries
```

This keeps the simulator stable even when RL library APIs or dependencies
change.

## Current Package Shape

The current implementation is organized as:

```text
aeroedge_rl/
  scenarios/uav_edge_service/
  adapters/
  baselines/
  experiments/
  rl/
```

The first implemented scenario is `uav_edge_service`, which models
UAV-assisted edge service orchestration with task generation, observations,
action masks, rewards, and metrics. It is an existing framework prototype.
The first formal teaching scenario is the planned static sensor TSP described
in [Two Research Tracks](lectures/research_tracks.md).

The current adapters include:

- Gymnasium environment wrapper;
- PettingZoo parallel multi-agent wrapper;
- RLlib multi-agent environment wrapper;
- RLlib action-mask model.

The current experiment entry points include:

- random rollout;
- no-RL demo;
- Gymnasium random rollout;
- PettingZoo random rollout;
- RLlib random rollout;
- RLlib PPO smoke test.

## Environment Strategy

Use a clean conda environment for RLlib-oriented development:

```text
conda env: aeroedge-rl
Python: 3.10
Primary libraries: Gymnasium, PettingZoo, RLlib, Torch, NumPy < 2
```

AgileRL should use a separate environment because its dependency constraints can
conflict with the RLlib stack:

```text
conda env: aeroedge-agilerl
Python: 3.11
Primary libraries: AgileRL, Gymnasium, PettingZoo
```

## Local GrADyS-SIM Import Rule

The project depends on the local `gradys-sim-nextgen` workspace during Phase 1.
Avoid relying on `PYTHONPATH` as the long-term mechanism because local
development can accidentally import an installed `gradysim` package instead of
the intended workspace package.

The recommended setup is editable installation of both local projects:

```bash
python -m pip install -e ../gradys-sim-nextgen --no-deps --no-build-isolation
python -m pip install -e . --no-deps --no-build-isolation
python scripts/check_environment.py
```

The environment checker should confirm that `gradysim` resolves to the local
`gradys-sim-nextgen` checkout.

This is not optional during the current research-development phase. Do not mix a
third-party installed `gradysim` package with the local simulator checkout when
running AeroEdgeRL experiments.

If a host uses a different directory layout, set:

```bash
export AEROEDGE_GRADYSIM_ROOT=/absolute/path/to/gradys-sim-nextgen
```

## Multi-Host Development Model

The intended workflow is:

```text
Mac
  architecture, documentation, package development, unit tests, CPU smoke tests

Windows GPU machine with RTX 5080
  WSL2 Ubuntu, CUDA, RLlib training, AgileRL experiments, long-running sweeps
```

There should be one source of truth: the remote Git repository. Do not maintain
separate drifting copies on different machines.

## Windows GPU Host Setup

Inside WSL2 Ubuntu, use the same repository layout when possible:

```text
~/Framework4test/
  gradys-sim-nextgen/
  AeroEdgeRL/
```

Then set up the RLlib environment:

```bash
cd ~/Framework4test/AeroEdgeRL
conda env create -f environment.yml
conda activate aeroedge-rl
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ../gradys-sim-nextgen --no-deps --no-build-isolation
python -m pip install -e . --no-deps --no-build-isolation
python scripts/check_environment.py
```

Before training, verify CUDA and Torch:

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

If Torch cannot see CUDA, fix the CUDA/PyTorch installation before debugging RL
training code.

## Useful Smoke Commands

Run these before expensive training:

```bash
pytest -q -p no:cacheprovider
python -m aeroedge_rl.experiments.cli.random_rollout
python -m aeroedge_rl.experiments.cli.gym_random
python -m aeroedge_rl.experiments.cli.pettingzoo_random
python -m aeroedge_rl.experiments.cli.rllib_random
```

Small PPO smoke test:

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

## Documentation System

The lecture and design documentation use Markdown with LaTeX math rendered by
MkDocs Material and MathJax.

Local preview:

```bash
conda activate aeroedge-rl
mkdocs serve
```

Open the local URL printed by MkDocs.

## Immediate Next Research Step

The next important technical boundary is:

> Define and test exactly how one RL step advances the GrADyS-SIM
> discrete-event simulator.

This boundary matters more than adding more algorithms. Once the simulator/RL
step semantics are stable, PPO/IPPO/MAPPO-style experiments can be made
reproducible.
