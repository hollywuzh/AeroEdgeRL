# Target Architecture

## Layered Design

```text
aeroedge_rl/
  sim/
    event.py
    simulator.py
    node.py
    handler.py
    protocol.py

  models/
    mobility/
    communication/
    energy/
    compute/
    workload/
    security/

  scenarios/
    uav_edge_service/
    uav_data_collection/
    uav_network_security/

  rl/
    core_env.py
    spaces.py
    observations.py
    actions.py
    rewards.py
    masks.py
    metrics.py

  adapters/
    gymnasium_env.py
    pettingzoo_parallel_env.py
    rllib_multiagent_env.py
    agilerl_env.py

  baselines/
    random.py
    nearest.py
    edf.py
    slo_risk.py

  experiments/
    runner.py
    registry.py
    callbacks.py
    logging.py
```

## Architectural Boundary

The most important boundary is this:

```text
sim/ and models/
  must not import Gymnasium, PettingZoo, RLlib, AgileRL, Ray, Torch, or JAX.

rl/
  may define RL concepts, but should remain backend-independent.

adapters/
  may import optional RL libraries.
```

## Core Abstractions

### Simulator

The simulator owns:

- event loop;
- simulated time;
- node registry;
- handler lifecycle;
- event execution;
- snapshot APIs.

### Scenario

A scenario owns:

- world initialization;
- agent list;
- workload generation;
- task lifecycle;
- reward rules;
- termination rules;
- metrics.

### CoreEnv

The core RL environment owns:

- `reset(seed=None)`;
- `step(actions)`;
- observation dict;
- reward dict;
- termination/truncation;
- info dict;
- action masks;
- snapshots.

It should not depend on Gymnasium or RLlib.

### Adapter

Adapters convert the same core environment into library-specific APIs:

- Gymnasium: centralized single-agent or vectorized controller view.
- PettingZoo: parallel multi-agent API.
- RLlib: `MultiAgentEnv` API.
- AgileRL: Gymnasium/PettingZoo-compatible wrappers and training utilities.

## Recommended Dependency Strategy

Core install:

```text
pip install aeroedge-rl
```

Optional installs:

```text
pip install aeroedge-rl[gym]
pip install aeroedge-rl[marl]
pip install aeroedge-rl[rllib]
pip install aeroedge-rl[agilerl]
pip install aeroedge-rl[all]
```

## Initial Package Extras

```toml
[project.optional-dependencies]
gym = ["gymnasium"]
marl = ["gymnasium", "pettingzoo"]
rllib = ["gymnasium", "ray[rllib]", "torch"]
agilerl = ["gymnasium", "pettingzoo", "agilerl"]
all = ["gymnasium", "pettingzoo", "ray[rllib]", "torch", "agilerl"]
```

