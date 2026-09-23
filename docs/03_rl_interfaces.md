# RL Interfaces

## Core Rule

The core environment should be backend-independent.

All RL libraries should consume this common result shape:

```python
observations, rewards, terminated, truncated, infos = env.step(actions)
```

For multi-agent scenarios:

```python
actions = {
    "uav_0": action_0,
    "uav_1": action_1,
}

observations = {
    "uav_0": obs_0,
    "uav_1": obs_1,
}
```

## Gymnasium Adapter

Gymnasium should be used for:

- centralized controller experiments;
- single-agent PPO baselines;
- quick smoke tests;
- compatibility with general RL tools.

Possible action space:

```text
MultiDiscrete([action_size] * num_uavs)
```

Possible observation:

```text
concat(obs[uav_0], obs[uav_1], ..., obs[uav_n])
```

## PettingZoo Adapter

PettingZoo ParallelEnv should be the default multi-agent standard because it
matches simultaneous UAV control naturally.

Expected shape:

```python
observations, infos = env.reset(seed=seed)
observations, rewards, terminations, truncations, infos = env.step(actions)
```

## RLlib Adapter

RLlib should use a dedicated `MultiAgentEnv` wrapper.

The wrapper should support:

- shared policy;
- independent policies;
- team reward;
- individual reward;
- action masking;
- global state for centralized critics;
- deterministic evaluation.

Terminations and truncations must include:

```python
terminateds["__all__"]
truncateds["__all__"]
```

## AgileRL Adapter

AgileRL integration should first reuse Gymnasium and PettingZoo-compatible
wrappers. A dedicated adapter should be added only when needed.

Target algorithms to evaluate later:

- PPO;
- IPPO;
- MADDPG;
- MATD3;
- MAPPO-style centralized critic if available or implemented through a custom
  training wrapper.

## Action Mask API

Action masks should be exposed by the core environment through a public method:

```python
env.action_mask(agent_id) -> list[float] | np.ndarray
```

Adapters may convert that into their expected format:

```python
{
    "observations": obs,
    "action_mask": mask,
}
```

Adapters must not inspect private scenario fields to construct masks.

## Global State API

For centralized critic methods, the core should provide:

```python
env.global_state() -> vector
```

This state can include:

- all UAV positions and velocities;
- pending task features;
- network condition summaries;
- energy summaries;
- deadline/slack summaries.

