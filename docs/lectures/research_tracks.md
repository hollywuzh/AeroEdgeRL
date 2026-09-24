# Two Research Tracks

This page records the agreed research and teaching direction. The first
formal problem is a [static sensor TSP](../scenarios/static_sensor_tsp.md).
The earlier dynamic edge-service demonstration is a runnable framework
prototype, not the first combinatorial teaching instance.

## Shared Foundation

Both tracks initially use the same static depot/sensor instances, GrADyS-SIM
discrete-event core, route executor, seeds, metric definitions, and trajectory
inspection. A track changes the decision interface and training problem; it
does not replace the simulator.

```text
GrADyS-SIM events -> AeroEdgeRL scenario -> shared evaluation
                                      |-> A: interactive policy
                                      |-> B: structured route planner
```

Lectures 00-01 establish the simulator foundation. Formal Lectures 02-04 will
define the static TSP and execute no-RL tours; they are planned, not yet
runnable. The old dynamic edge-service example remains under Scenarios.

## Track A: Interactive RL

For the first comparison, an interactive policy observes the current UAV
position and unvisited sensor set, then selects the next unvisited sensor.
The same static TSP instance is used by Track B. The policy must return to
the depot after the last visit. Gymnasium/RLlib adapters may support this
interface; the existing PPO smoke test targets the older edge-service
prototype and is not TSP training evidence.

Input and output:

```text
current node + unvisited mask -> policy -> next sensor action
  -> simulator events -> next observation + reward
```

This track studies sequential action learning. It starts with a small
learnability test against valid random-next-node and nearest-neighbor. Scale
only after tour validity, tour cost, learning curves, and trajectories are
interpretable. Long training without improvement calls for diagnosing
observation coverage, masks, reward density, and delayed credit.

## Track B: Combinatorial RL

The first structured instance contains one depot, fixed sensor coordinates,
and pairwise Euclidean travel costs. A route-construction or improvement
policy outputs one permutation before departure. The route executor applies
the plan through the same GrADyS simulator.

Input and output:

```text
depot + sensor graph -> route solver -> ordered stops
  -> executor -> simulator events -> completed tour and trajectory
```

The first teaching instance is a small closed Euclidean TSP: every sensor is
mandatory; the UAV starts and ends at the depot. Compare a learned route with
LKH as the primary heuristic and nearest-neighbor as a sanity check. Task
value, deadlines, dynamic arrivals, and multi-UAV assignment are outside the
initial scenario. Later additions require a new formal problem statement;
they may lead to orienteering or vehicle-routing variants.

The route-learning implementation may use a dedicated neural combinatorial
optimization training loop. It need not be forced through RLlib's step-action
API. Its trained checkpoint is an inference component at the planning
boundary; the execution and evaluation remain in AeroEdgeRL.

## Later Bridge: Plan, Execute, Replan

After A and B are independently understandable, compare a hybrid controller:
the route planner proposes a plan, the simulator executes it, and an online
decision rule determines whether and when to replan. This is a later bridge
between the two tracks, not a prerequisite for the first TSP lesson.

Replanning is outside the first static TSP lesson. When a later scenario
introduces changing inputs, define its trigger and record plan age,
replanning frequency, inference latency, and executed-route quality.

## Comparison Contract

| Item | Track A | Track B |
| --- | --- | --- |
| Decision object | One next-sensor action after each visit. | One sensor permutation before departure. |
| Training data | Static TSP transitions and rewards. | Static TSP instances and route-level cost signals. |
| First sanity baseline | Valid random-next-node and nearest-neighbor. | LKH primary heuristic; nearest-neighbor sanity check. |
| Shared outcome | Valid visits, closed tour length, executed distance/time, trajectory. | The same executed-scenario outcomes. |
| Extra diagnostic | Learning curve, invalid actions, inference time per choice. | Tour gap, permutation validity, whole-plan inference time. |

Compare the tracks on the same held-out TSP instances and seeds. Report
training cost separately from inference latency and executed-tour quality.
A shorter abstract tour does not automatically imply a shorter simulated
path when mobility dynamics are taken into account.

## Open Design Questions

These require explicit decisions during the first TSP implementation:

1. What is the exact map from a planned stop to a simulator action and
   completion event?
2. Which exact small-instance solver and held-out instance generator define
   a proven optimum when needed? LKH itself does not certify optimality.
3. What minimum learnability result lets Track A grow beyond a smoke test?

Until the static TSP generator and executor exist, formal Lectures 02-04
remain planned. The dynamic edge-service prototype stays available for
testing framework plumbing.
