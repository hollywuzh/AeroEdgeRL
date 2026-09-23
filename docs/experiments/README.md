# Experiments

This section records how AeroEdgeRL experiments are run, checked, compared, and
interpreted.

Experiments should be reproducible from commands and configuration, not from
memory.

## Experiment Principle

Every meaningful experiment should record:

- git commit hash;
- host machine;
- conda environment;
- GrADyS-SIM source path or commit;
- exact command;
- scenario configuration;
- random seed list;
- algorithm configuration;
- metrics output path;
- trajectory output path;
- summary result.

## Experiment Levels

Use three levels.

### Smoke

Smoke experiments answer:

```text
Does the code path run?
```

They can be short, CPU-friendly, and statistically meaningless.

### Sanity

Sanity experiments answer:

```text
Does the behavior make sense?
```

They should compare random and heuristic policies, inspect metrics, and render
trajectories.

### Research

Research experiments answer:

```text
Does the method improve over interpretable baselines under repeated seeds?
```

They require multiple seeds, stable metrics, visual checks, and enough training
budget to support a claim.

## Current Smoke Commands

```bash
python scripts/check_environment.py
pytest -q -p no:cacheprovider
python -m aeroedge_rl.experiments.cli.random_rollout
python -m aeroedge_rl.experiments.cli.gym_random
python -m aeroedge_rl.experiments.cli.pettingzoo_random
python -m aeroedge_rl.experiments.cli.rllib_random
```

Small PPO smoke:

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

## Windows GPU Role

The Windows GPU machine should run longer training jobs inside WSL2 Ubuntu.

The Mac remains the primary place for:

- documentation;
- code design;
- unit tests;
- CPU smoke tests.

The Windows GPU machine is for:

- RLlib training;
- multi-seed sweeps;
- checkpoint generation;
- longer PPO/IPPO/MAPPO experiments.
