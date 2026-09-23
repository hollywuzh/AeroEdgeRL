# Contributing And Local Setup

This project uses a two-workspace development model during Phase 1:

```text
Framework4test/
  gradys-sim-nextgen/   # local GrADyS-SIM simulator workspace
  AeroEdgeRL/           # RL-first framework workspace
```

AeroEdgeRL depends on the local GrADyS-SIM workspace through an editable install.
Do not rely on `PYTHONPATH` as the normal development workflow.

## Quick Start From A Fresh Clone

Clone both repositories as siblings:

```bash
mkdir -p ~/Framework4test
cd ~/Framework4test
git clone <gradys-sim-nextgen-url> gradys-sim-nextgen
git clone <aero-edge-rl-url> AeroEdgeRL
```

Create and activate the conda environment:

```bash
cd AeroEdgeRL
conda env create -f environment.yml
conda activate aeroedge-rl
python -m pip install --upgrade pip setuptools wheel
```

Install both local workspaces in editable mode:

```bash
python -m pip install -e ../gradys-sim-nextgen --no-deps --no-build-isolation
python -m pip install -e . --no-deps --no-build-isolation
```

Validate the environment:

```bash
python scripts/check_environment.py
pytest -q -p no:cacheprovider
python -m aeroedge_rl.experiments.cli.random_rollout
python -m aeroedge_rl.experiments.cli.gym_random
python -m aeroedge_rl.experiments.cli.pettingzoo_random
```

If your two repositories are not siblings, set:

```bash
export AEROEDGE_GRADYSIM_ROOT=/absolute/path/to/gradys-sim-nextgen
```

before running:

```bash
python scripts/check_environment.py
```

## Mac Development Role

Use the Mac environment for:

- documentation;
- framework design;
- package migration;
- unit tests;
- CPU smoke tests;
- Gymnasium/PettingZoo interface checks.

## Windows GPU Role

Use Windows as the host OS, but run GPU training inside WSL2 Ubuntu.

Inside WSL2, use the same clone layout and the same conda environment name:

```bash
conda env create -f environment.yml
conda activate aeroedge-rl
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ../gradys-sim-nextgen --no-deps --no-build-isolation
python -m pip install -e . --no-deps --no-build-isolation
python -m pip install "ray[rllib]" torch "numpy<2"
```

For AgileRL experiments:

```bash
conda env create -f environment-agilerl.yml
conda activate aeroedge-agilerl
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ../gradys-sim-nextgen --no-deps --no-build-isolation
python -m pip install -e . --no-deps --no-build-isolation
```

Validate GPU availability before long training runs:

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

If CUDA is not available in PyTorch, reinstall the PyTorch build that matches
the machine's driver and CUDA setup before running RLlib or AgileRL training.

## Repository Hygiene

Keep source code, docs, configs, and tests in git.

Do not commit:

- `outputs/`;
- `checkpoints/`;
- `.venv/`;
- `.pytest_cache/`;
- generated logs;
- large datasets;
- large model checkpoints.

Training results should be summarized in markdown/CSV/JSON references, while
large artifacts stay outside git unless a later artifact-management workflow is
defined.

## Import Invariant

The following must be true in every development environment:

```text
import gradysim
```

must resolve to the local `gradys-sim-nextgen` clone, not to an older installed
package in site-packages.

Always run:

```bash
python scripts/check_environment.py
```

after creating a new environment or pulling major dependency changes.
