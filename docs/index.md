# AeroEdgeRL

AeroEdgeRL is an RL-first UAV edge intelligence simulation framework built
around a preserved GrADyS-SIM discrete-event core.

The documentation has two tracks:

- the project design docs, which record architecture and environment decisions;
- the lecture notes, which teach the simulator first and then introduce RL
  algorithms with runnable experiments.

## Start Here

If you are learning the framework, begin with:

1. [Lecture Notes](lectures/README.md)
2. [Simulation-First Roadmap](lectures/00_simulation_first_roadmap.md)
3. [GrADyS Core In AeroEdgeRL](lectures/01_gradys_core_in_aeroedge.md)
4. [No-RL UAV Edge Service Demo](lectures/02_no_rl_uav_edge_demo.md)

## Math Rendering

Lecture notes are written in Markdown with LaTeX math rendered by MathJax.

Inline math uses `\( ... \)`, for example \(Q(s,a)\).

Display math uses `\[ ... \]`:

\[
G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}.
\]

This keeps the lectures readable in source form while still supporting formal
mathematical exposition in the generated documentation site.
