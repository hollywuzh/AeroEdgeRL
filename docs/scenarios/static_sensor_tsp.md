# Static Sensor TSP: First Teaching Problem

This is the first **planned** formal teaching scenario. It isolates a small
combinatorial routing problem while GrADyS-SIM executes UAV movement. The
existing dynamic edge-service demo is a separate runnable prototype; it is
not evidence that the TSP scenario already runs.

## Problem Boundary

One UAV starts at a fixed depot \(p_0\). A fixed set of \(n\) sensors at
\(p_1,\ldots,p_n\) must each be visited exactly once. The UAV returns to
the depot. Positions are known before planning and do not change.

The first version has one UAV, one depot, symmetric Euclidean costs, and
mandatory visits. It excludes task value, deadline, queue, dynamic arrival,
offloading, communication decisions, and resource allocation. A visit is
recorded only when the UAV reaches the *currently commanded* sensor's visit
radius. Passing near a different sensor does not reorder or complete the tour.

The planner chooses a permutation \(\pi\) of sensor IDs. With \(\pi_0=0\)
and \(\pi_{n+1}=0\), minimize the closed-tour length:

\[
L(\pi)=\sum_{k=0}^{n}\left\|p_{\pi_{k+1}}-p_{\pi_k}\right\|_2.
\]

The depot start and return convention is identical for every solver.

## Routing-Only Variant Ladder

After the closed Euclidean TSP works, vary one routing assumption at a time:

| Variant | Single changed assumption | First new check |
| --- | --- | --- |
| Open-path TSP | End at the last sensor instead of returning to depot. | Start/end convention and path cost. |
| Asymmetric TSP | Directed travel costs can differ by direction. | Cost matrix and direction-aware baselines. |
| Multiple-TSP | Several UAVs partition mandatory sensors. | Every sensor assigned once; per-UAV tours and balance. |

These are later routing lessons, not hidden options in the first closed-tour
experiment. Task values, deadlines, and dynamic arrivals are deferred to
separate service-oriented scenarios with new objectives and baselines.

## Planning And Simulation Contracts

| Boundary | Input | Output |
| --- | --- | --- |
| Instance generator | Seed, area, sensor count | Depot and stable sensor IDs/coordinates. |
| Route solver | Depot, sensors, distance matrix | Valid permutation of every sensor ID. |
| Route executor | Ordered IDs, visit radius, mobility settings | GrADyS movement commands and visit events. |
| Evaluator | Plan and executed trace | Tour length, executed distance/time, validity, trajectory. |

Every solver receives the same instance. The executor validates duplicate or
missing IDs before commanding the UAV. It records the abstract route and the
actual GrADyS trajectory; mobility is simulated, not teleported.

## First No-RL Milestone

A seeded 5-10 sensor instance should be solved with LKH as the primary
heuristic route baseline, then executed in GrADyS-SIM. Nearest-neighbor may
remain as a transparent sanity check, but is not the main benchmark. Save:

- instance JSON with depot and sensor coordinates;
- ordered sensor IDs and abstract tour length;
- execution trace with timestamped positions and visit events;
- a readable plot with numbered sensors, depot, and travel direction;
- a table of route validity, planned length, executed distance, and time.

Use `aeroedge_rl.baselines.lkh.solve_lkh(points)` with point 0 as the depot.
It returns a depot-first route ending at the depot and its continuous
Euclidean length. Set `AEROEDGE_LKH_BINARY` to the host's LKH executable or
pass `binary=` explicitly. The adapter writes an integer-scaled TSPLIB
distance matrix for LKH; the reported route length is recomputed using the
original floating-point coordinates. Record LKH version, seed, scale and
runtime for comparisons. LKH is a strong heuristic, **not an exact solver or
optimality certificate**. Use an exact solver separately if a proven optimum
is needed for very small instances.

The executable is an external research dependency, not an AeroEdgeRL
component. This repository keeps backup copies under `third_party/lkh/` so
that the macOS development machine and the Windows GPU machine can reproduce
the same baseline setup. The macOS binary is arm64 and cannot run on Windows;
the Windows host should use `third_party/lkh/LKH-3.exe` or build from source
inside WSL/Linux. Always set `AEROEDGE_LKH_BINARY` explicitly on each host.

Official downloads are available from the
[LKH-3 author page](http://webhotel4.ruc.dk/~keld/research/LKH-3/):
`LKH-3.0.13.tgz` (source) and `LKH-3.exe` (Windows x64). On macOS, compile
the source with `make` to obtain an arm64 `LKH`. A local cache may also be
kept under `.local/lkh/`, which Git ignores. The author's page permits
academic and non-commercial use while reserving rights; treat the files in
`third_party/lkh/` as research-only backup artifacts and keep the upstream
source and checksum information visible.

## Graduation To Learning

Only after no-RL routes execute correctly should a neural combinatorial
policy learn to output a permutation. Compare it on held-out static instances
and execute its tours in the same simulator. Interactive RL, which chooses one
action per control boundary, is a separate research track.

Introduce routing-only TSP variants one modeling change at a time. Optional
visits, values, deadlines, or dynamic arrivals belong to later scenarios and
require a revised objective, feasible set, baselines, and evaluation.

## Status

The mathematical contract is fixed for the first lesson. The generator,
GrADyS executor, plot, and lectures are **planned**. The external LKH route
adapter is available, but the full TSP simulation loop is not yet runnable.
