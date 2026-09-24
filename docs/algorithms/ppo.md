# PPO

Proximal Policy Optimization is the first practical deep RL algorithm to use as
an AeroEdgeRL training target.

This page is a placeholder for the detailed lecture and implementation plan.

## Why PPO First

PPO is a reasonable first training algorithm because:

- RLlib supports it well;
- it works with discrete action spaces;
- it can be adapted to shared-policy multi-agent training;
- it gives a useful bridge from Gymnasium to RLlib;
- it is easier to stabilize than many off-policy deep RL methods.

## AeroEdgeRL Use

The existing PPO smoke experiment targets the dynamic UAV edge-service
prototype. It verifies adapter wiring, not the first formal static TSP
teaching problem or a trained policy result.

The expected progression is:

```text
Gymnasium centralized PPO smoke test
  -> RLlib single-policy PPO
  -> RLlib shared-policy multi-agent PPO
  -> action-masked PPO
  -> multi-seed evaluation
```

## Minimum Experiment

The minimum PPO experiment should be small enough to run quickly on a CPU, but
structured enough to validate the full training path:

- one UAV;
- a few ground devices;
- short episode duration;
- small train batch;
- deterministic seed;
- JSON metrics output.

The current smoke command is:

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

This is not a research result. It only proves that the training stack is wired
correctly.
