# Lecture Design

This page defines how the AeroEdgeRL lecture notes are written and reviewed.
The [course map](README.md#course-map) lists individual lectures and their
status. Read this design once, then follow the map in order.

The lecture sequence should teach three things together:

- discrete-event UAV edge simulation;
- heuristic closed-loop scenario validation;
- reinforcement-learning algorithm reproduction.

## Lecture Principle

The lectures follow a simulation-first principle:

```text
simulation semantics
  -> scenario closed loop
  -> heuristic baseline
  -> RL formulation
  -> RL algorithm
  -> experiment and visualization
```

The GrADyS-SIM discrete-event engine owns simulated time, event scheduling,
handlers, mobility, and node protocols. AeroEdgeRL owns scenarios and their
decision boundaries. Heuristic and RL policies operate at those boundaries.
Every lecture should make the boundary it uses visible.

## Part I: Simulation First

Part I explains why AeroEdgeRL starts from the simulator rather than from a
neural-network training loop.

The reader first checks the local simulator import, then follows a UAV edge
service task from arrival through policy choice, movement, completion or
expiry, and metric recording. A heuristic baseline closes this loop before
the first learning algorithm is introduced.

Expected outcome:

```text
The reader can run and explain a UAV edge-service simulation without RL.
```

## Part II: RL Foundations

Part II introduces reinforcement-learning theory through the simulator-facing
contract.

The same scenario is mapped to states or observations, legal actions, rewards,
transitions, and episode endings. Return, value functions, Bellman equations,
dynamic programming, Monte Carlo methods, and temporal-difference control are
introduced in that order. Small tabular experiments should expose each update
rule and compare it against the heuristic baseline.

Expected outcome:

```text
The reader can explain what the simulator must provide to an RL algorithm.
```

## Part III: Deep RL

Part III moves from tabular algorithms to function approximation and practical
deep RL.

Function approximation leads to DQN, policy gradients, actor-critic methods,
and PPO. Each algorithm lecture should connect its objective and update rule
to the framework's actual observation, action mask, reward, and episode API.
The existing RLlib PPO smoke command only checks that the pipeline runs;
training quality requires a separate evaluation.

Expected outcome:

```text
The reader can reproduce a small PPO experiment and interpret its metrics.
```

## Part IV: Multi-Agent RL

Part IV extends the framework from a centralized controller to multiple UAV
agents.

Multiple UAVs add simultaneous decisions, agent identity, shared resources,
and coordination. PettingZoo and RLlib adapters should be explained from the
same core scenario. Independent policies, shared policies, and centralized
critics must state exactly which information is available during execution
and during training.

Expected outcome:

```text
The reader can map a UAV swarm scenario to a multi-agent RL interface.
```

## Part V: Research Experiments

Part V explains how to turn a scenario and an algorithm into a research-grade
experiment.

Each new research scenario begins with a no-RL demonstration and an
interpretable heuristic closed loop. Experiments progress from smoke checks
to behavioral sanity checks and then multi-seed research comparisons.
Reports include configuration, seeds, commands, metrics, and UAV trajectory
plots. A trajectory plot must let the reader distinguish purposeful movement
from confusing crossing lines.

Expected outcome:

```text
The reader can produce a reproducible experiment with metrics and interpretable
trajectory plots.
```

## Standard Lecture Template

Each lecture should use the same structure. A planned lecture becomes
"current" in the course map only when its command or example matches an
available artifact and its expected observations are described.

### Learning Goals

State observable outcomes: what the reader can derive, run, or inspect.

### Problem Background

Why does this topic matter for UAV edge intelligence and discrete-event RL?

### Theory

Define variables and assumptions before equations. Derive the result needed
for the scenario, and state where an approximation enters. For an RL update,
identify the data required at each control step and explain whether time is
measured in simulator events or decision intervals.

Use LaTeX math when needed, for example:

\[
G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}.
\]

### AeroEdgeRL Contract

Give a compact input/output contract in framework terms:

- simulator state;
- observation;
- action;
- reward;
- termination or truncation;
- metrics;
- trajectory data, when the artifact records it.

Name the owner of each quantity: GrADyS-SIM core, AeroEdgeRL scenario,
adapter, policy, or experiment runner. Do not imply an artifact contains
positions, checkpoints, or diagnostics that it does not actually write.

### Minimal Runnable Example

Give a command that runs from the repository in the `aeroedge-rl` environment.
Specify the seed, small scenario configuration, and output path. Link the
relevant source or CLI when interpretation depends on implementation details.

### Simulation or Training Effect

Explain what the reader should observe:

- metrics;
- logs;
- rendered trajectories;
- policy behavior;
- failure modes.

Separate a successful command, plausible behavior, and evidence for a
research claim. Report observed results only after running the command;
otherwise describe the expected output shape and what to check.

### Common Mistakes

Record likely traps:

- importing the wrong `gradysim`;
- treating a smoke test as a research result;
- comparing RL without a heuristic baseline;
- ignoring trajectory visualization;
- confusing simulator time with wall-clock time.

### Next Step

Point to the next lecture or experiment.

## Relationship To Other Documentation

The lecture notes are the narrative path.

Other sections have different roles:

- `Scenarios` defines benchmark families and scenario artifacts;
- `Algorithms` records algorithm-specific reproduction plans;
- `Experiments` records execution, evaluation, and reporting protocols;
- `Project Docs` records architecture and environment decisions.

The same idea may appear in multiple places, but with different purposes. For
example, PPO appears:

- in `Algorithms` as an algorithm plan;
- in `Experiments` as a runnable command;
- in `Lecture Notes` as a teachable concept;
- in `Scenarios` as a method applied to a concrete UAV problem.

## Reading Order

The [course map](README.md#course-map) is the source for lecture status.
After this design page, continue to
[Lecture 00: Simulation-First Roadmap](00_simulation_first_roadmap.md).
The Part I sequence then explains the GrADyS core, runs the no-RL scenario,
compares heuristics, and inspects UAV trajectories before Part II formalizes
the learning problem.
