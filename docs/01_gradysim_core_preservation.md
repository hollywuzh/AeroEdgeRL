# GrADyS Core Preservation

## Non-Negotiable Requirement

AeroEdgeRL must keep the GrADyS-SIM discrete-event simulation core.

The current GrADyS-SIM codebase already has the pieces that matter:

- `EventLoop`: schedules and pops timestamped simulation events.
- `Simulator`: owns the event loop, nodes, handlers, initialization,
  finalization, and single-event stepping.
- `SimulationBuilder`: builds scenarios from handlers and protocol nodes.
- `Node`: stores node identity, position, and protocol encapsulator.
- `IProtocol` and `IProvider`: define how node logic interacts with the
  simulated world.
- `INodeHandler`: defines simulator capabilities such as timer,
  communication, mobility, radio, camera, and visualization.
- `DynamicVelocityMobilityHandler`: provides velocity-based UAV mobility with
  speed and acceleration constraints.

## What We Preserve

The following concepts should be preserved as first-class framework elements:

```text
EventLoop
  -> Event(timestamp, callback, context)
  -> schedule_event()
  -> pop_event()
  -> current_time

Simulator
  -> step_simulation()
  -> start_simulation()
  -> is_simulation_done()
  -> node registry
  -> handler lifecycle

Handler
  -> inject(event_loop)
  -> register_node(node)
  -> initialize()
  -> after_simulation_step()
  -> finalize()

Protocol / Provider
  -> initialize()
  -> handle_timer()
  -> handle_packet()
  -> handle_telemetry()
  -> finish()
```

## What We Improve

The RL version needs clearer control boundaries:

- Add an official `advance_until(target_time)` or equivalent simulator method.
- Define how many discrete events may occur inside one RL control interval.
- Expose simulator snapshots without relying on private fields.
- Separate scenario state from adapter state.
- Add deterministic seeding for event scheduling, mobility, task generation,
  communication failure, and workload sampling.
- Provide public APIs for action masks, global state, per-agent state, metrics,
  and episode termination.

## What We Avoid

AeroEdgeRL should not:

- Turn the simulator into a fixed-step Gym loop.
- Let RL libraries directly mutate node positions or event queues.
- Hide event-driven behavior behind an opaque training script.
- Let RLlib or AgileRL-specific assumptions leak into the simulator core.

## Target Control Flow

```text
RL policy
  -> action dict
  -> AeroEdgeRL CoreEnv.step(actions)
  -> action decoder
  -> protocol/provider commands
  -> GrADyS EventLoop advances until control boundary
  -> handlers update mobility/communication/timers
  -> scenario computes reward and termination
  -> observations/rewards/infos returned to adapter
```

