# AeroEdgeRL

AeroEdgeRL is an RL-first UAV edge intelligence simulation framework.

The project starts from one non-negotiable architectural decision:

> AeroEdgeRL must preserve the discrete-event simulation core of GrADyS-SIM.

RL libraries such as Gymnasium, PettingZoo, RLlib, and AgileRL are treated as
interfaces and training backends. They do not replace the simulator core. The
simulator remains responsible for event scheduling, simulated time, nodes,
communication, mobility, telemetry, and scenario dynamics.

## Project Positioning

AeroEdgeRL targets research on UAV-assisted edge intelligence, multi-agent
reinforcement learning, service orchestration, low-altitude networking, and
event-driven cyber-physical simulation.

The framework will evolve around three ideas:

- Keep GrADyS-SIM's discrete-event kernel as the simulation foundation.
- Add a clean RL environment layer with observations, actions, rewards,
  episode lifecycle, action masks, metrics, and reproducible seeds.
- Provide standard adapters for Gymnasium, PettingZoo, RLlib, and AgileRL.

## Initial Documentation Map

- [Project Charter](docs/00_project_charter.md)
- [GrADyS Core Preservation](docs/01_gradysim_core_preservation.md)
- [Target Architecture](docs/02_target_architecture.md)
- [RL Interfaces](docs/03_rl_interfaces.md)
- [Phase 1 Migration Design](docs/04_phase1_migration_design.md)
- [Phase 1 Implementation Plan](docs/05_phase1_implementation_plan.md)
- [Development Environment](docs/06_development_environment.md)
- [Multi-Host Development Model](docs/07_multi_host_development_model.md)
- [AgileRL Adapter Plan](docs/08_agilerl_adapter_plan.md)
- [Project Context Handoff](docs/09_project_context_handoff.md)
- [Lecture Notes](docs/lectures/README.md)
- [Roadmap](roadmap/ROADMAP.md)
- [ADR-0001: Preserve GrADyS Discrete Event Core](design/adr/0001-preserve-gradysim-event-core.md)
- [Current GrADyS Audit Notes](references/gradysim_audit.md)

## Working Principle

This repository begins as a documentation-driven project. Code should be added
only after the project documents define the boundary, vocabulary, and migration
plan clearly enough to keep the framework controllable.

## Development Baseline

The initial Python package is intentionally lightweight:

```bash
python -m pip install -e .
python -c "import aeroedge_rl; print(aeroedge_rl.__version__)"
```

Optional RL libraries are installed through extras such as `gym`, `marl`,
`rllib`, and `agilerl`; importing `aeroedge_rl` itself should not import any of
those heavy backends.

During Phase 1, AeroEdgeRL uses the local GrADyS-SIM workspace as its simulator
backend. The recommended workflow is a clean conda environment with editable
installs for both local projects:

```bash
conda create -n aeroedge-rl python=3.10 -y
conda activate aeroedge-rl
python -m pip install --upgrade pip setuptools wheel
python -m pip install "websockets>=12" "pandas>=2.2.3" "aiohttp>=3.11.14" "gymnasium==1.1.1" "numpy<2" "pettingzoo==1.26.1" "ray[rllib]" torch pytest ruff
python -m pip install -e /Users/wupengfei/Documents/Framework4test/gradys-sim-nextgen --no-deps --no-build-isolation
python -m pip install -e /Users/wupengfei/Documents/Framework4test/AeroEdgeRL --no-deps --no-build-isolation
python scripts/check_environment.py
```

`PYTHONPATH` is only a temporary rescue path before the editable installs are
set up. See [Development Environment](docs/06_development_environment.md).

AgileRL uses a separate Python 3.11 environment; see
[AgileRL Adapter Plan](docs/08_agilerl_adapter_plan.md).

For multi-host development and GPU training, see
[Multi-Host Development Model](docs/07_multi_host_development_model.md) and
[Contributing And Local Setup](CONTRIBUTING.md).

## Lecture Website

The lecture notes are Markdown files with LaTeX math rendered by MathJax through
MkDocs Material:

```bash
conda activate aeroedge-rl
cd /Users/wupengfei/Documents/Framework4test/AeroEdgeRL
mkdocs serve
```

Then open the local URL printed by MkDocs.

## Online Documentation

The repository includes a GitHub Actions workflow for publishing the MkDocs site
to GitHub Pages.

In the GitHub repository, enable:

```text
Settings -> Pages -> Build and deployment -> Source -> GitHub Actions
```

After that, every push to `main` builds and deploys the documentation site.
