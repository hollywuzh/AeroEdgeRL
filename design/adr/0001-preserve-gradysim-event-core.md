# ADR-0001: Preserve GrADyS Discrete Event Core

## Status

Accepted.

## Context

The current GrADyS-SIM framework already provides a clean event-driven
simulation architecture. It is built around timestamped events, handlers,
protocols, providers, and simulation nodes.

AeroEdgeRL aims to introduce reinforcement learning support through Gymnasium,
PettingZoo, RLlib, and AgileRL. However, those libraries are environment and
training interfaces. They should not define the simulator's internal time model.

## Decision

AeroEdgeRL will preserve the GrADyS-SIM discrete-event simulation core.

The RL layer will be built as a control and observation layer above the
simulator:

```text
RL algorithm
  -> adapter
  -> core RL environment
  -> scenario logic
  -> GrADyS event simulator
```

The simulator remains responsible for:

- event scheduling;
- simulated time;
- node lifecycle;
- handler lifecycle;
- mobility updates;
- communication events;
- telemetry delivery.

## Consequences

Positive:

- Keeps the simulator suitable for network and cyber-physical systems.
- Avoids reducing everything to fixed-step array simulation.
- Makes mobility, communication, and timers composable.
- Allows realistic asynchronous events inside one RL control interval.

Tradeoffs:

- RL step semantics must be carefully documented.
- Event-aligned time can differ from the requested control interval.
- Tests must cover event advancement and episode boundaries.
- Adapters need to hide event complexity without erasing it.

## Follow-Up Work

- Add public simulator advancement APIs.
- Add public snapshot APIs.
- Add deterministic seeding across simulator and scenario components.
- Add tests that bind RL step behavior to event-loop behavior.

