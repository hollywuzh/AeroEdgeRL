# Multi-Host Development Model

## Decision

AeroEdgeRL uses a split development model:

```text
Mac
  -> primary development host
  -> docs, architecture, package migration, unit tests, CPU smoke tests

Windows GPU machine with RTX 5080
  -> training host
  -> WSL2 Ubuntu, CUDA, RLlib, AgileRL, long-running experiments
```

Both machines should use the same repository structure and the same conda
environment name:

```text
Framework4test/
  gradys-sim-nextgen/
  AeroEdgeRL/

conda env:
  aeroedge-rl       # RLlib/Gymnasium/PettingZoo
  aeroedge-agilerl  # AgileRL, Python 3.11
```

## Why This Model

The framework has two very different workloads:

- engineering work: frequent edits, tests, documentation, refactoring;
- training work: heavy GPU runs, Ray workers, checkpoints, multi-seed sweeps.

The Mac is better for the first workload. The Windows GPU machine is better for
the second, but should run the Linux training stack inside WSL2 Ubuntu to reduce
Windows-native Ray/RLlib friction.

## Repository Rule

There is one source of truth:

```text
git repository on GitHub
```

Do not maintain separate drifting copies of the project on different machines.

Use:

```bash
git pull
git status
git diff
```

to move source changes between machines.

Use configs and seeds to reproduce experiments. Do not manually patch training
scripts on the GPU machine without committing or recording the change.

## Clone Layout

Preferred layout on every machine:

```text
~/Framework4test/
  gradys-sim-nextgen/
  AeroEdgeRL/
```

If a host uses a different layout, set:

```bash
export AEROEDGE_GRADYSIM_ROOT=/absolute/path/to/gradys-sim-nextgen
```

The environment checker uses this variable to verify that `gradysim` resolves
to the intended simulator workspace.

## Mac Setup

```bash
cd ~/Framework4test/AeroEdgeRL
conda env create -f environment.yml
conda activate aeroedge-rl
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ../gradys-sim-nextgen --no-deps --no-build-isolation
python -m pip install -e . --no-deps --no-build-isolation
python scripts/check_environment.py
pytest -q -p no:cacheprovider
python -m aeroedge_rl.experiments.cli.random_rollout
python -m aeroedge_rl.experiments.cli.gym_random
python -m aeroedge_rl.experiments.cli.pettingzoo_random
```

Optional Mac training-adapter smoke layer:

```bash
python -m pip install "ray[rllib]"
python -m pip install torch
python -m pip install "numpy<2"
python -m aeroedge_rl.experiments.cli.rllib_random --output /tmp/aeroedge_rllib_random_rollout.jsonl
python -m aeroedge_rl.experiments.cli.rllib_ppo_smoke --iterations 1 --num-uavs 1 --num-devices 3 --episode-duration 3 --candidate-limit 2 --train-batch-size 16 --minibatch-size 8 --rollout-fragment-length 4 --num-epochs 1 --quiet --output /tmp/aeroedge_rllib_ppo_smoke_metrics.json
```

## WSL2 GPU Setup

Inside WSL2 Ubuntu:

```bash
cd ~/Framework4test/AeroEdgeRL
conda env create -f environment.yml
conda activate aeroedge-rl
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ../gradys-sim-nextgen --no-deps --no-build-isolation
python -m pip install -e . --no-deps --no-build-isolation
python -m pip install "ray[rllib]" torch "numpy<2"
python scripts/check_environment.py
```

AgileRL uses a separate Python 3.11 environment:

```bash
conda env create -f environment-agilerl.yml
conda activate aeroedge-agilerl
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ../gradys-sim-nextgen --no-deps --no-build-isolation
python -m pip install -e . --no-deps --no-build-isolation
python scripts/check_environment.py
```

GPU sanity checks:

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

If `torch.cuda.is_available()` returns `False`, fix the PyTorch/CUDA install
before running training. Do not debug RL algorithms until the GPU stack is
confirmed.

## What Runs Where

| Task | Mac | WSL2 GPU |
| --- | --- | --- |
| Architecture docs | Yes | Optional |
| Core simulator bridge development | Yes | Optional |
| Unit tests | Yes | Yes |
| Random rollout smoke tests | Yes | Yes |
| Gymnasium adapter checks | Yes | Optional |
| PettingZoo adapter checks | Yes | Optional |
| RLlib random rollout | Optional | Yes |
| PPO/IPPO/MAPPO training | No | Yes |
| Multi-seed sweeps | No | Yes |
| Checkpoint evaluation | Optional | Yes |

## Artifacts

Keep generated artifacts out of git:

```text
outputs/
checkpoints/
```

For each important training run, record:

- git commit hash;
- machine;
- conda environment;
- exact command;
- config;
- seed list;
- output directory;
- summary metrics.

Large artifacts should stay on the training machine or a dedicated artifact
store. Only compact summaries should be committed unless a later workflow uses
DVC, Git LFS, or another artifact manager.

## Pull Request Checklist

Before pushing code from either machine:

```bash
python scripts/check_environment.py
pytest -q -p no:cacheprovider
git status
```

For training-related changes, also record:

```bash
python -m aeroedge_rl.experiments.cli.random_rollout
```

and, when RLlib is installed:

```bash
python -m aeroedge_rl.experiments.cli.rllib_random
```

The RLlib command may not exist until the RLlib adapter migration step is
complete.
