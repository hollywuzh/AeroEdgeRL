# GrADyS-SIM Dependency Strategy

This document defines how AeroEdgeRL should depend on GrADyS-SIM.

The rule is intentionally strict because importing the wrong `gradysim` package
would make experiments non-reproducible.

## Decision

During the current research-development phase, AeroEdgeRL uses a local
`gradys-sim-nextgen` checkout installed in editable mode.

The expected repository layout is:

```text
Framework4test/
  gradys-sim-nextgen/
  AeroEdgeRL/
```

The expected installation order is:

```bash
conda activate aeroedge-rl
python -m pip install -e ../gradys-sim-nextgen --no-deps --no-build-isolation
python -m pip install -e . --no-deps --no-build-isolation
python scripts/check_environment.py
```

This means the active Python environment should import:

```text
../gradys-sim-nextgen/gradysim
```

not an unrelated package from `site-packages`.

## Why Local Checkout First

The framework is being designed around GrADyS-SIM's discrete-event core.
During this phase, we need to inspect behavior, preserve event semantics, and
possibly adapt to local source changes.

A third-party installed package is not appropriate as the primary development
source because:

- it may be older than the local simulator code;
- it may not contain the same handlers or configuration objects;
- it hides source changes from Git review;
- it can be accidentally imported by Ray workers or notebooks;
- it makes Mac and Windows/WSL2 behavior harder to compare.

## Third-Party Package Policy

There are two valid modes.

### Research Development Mode

Use this mode now.

```text
source: local sibling checkout
install: editable
validation: scripts/check_environment.py
```

This is the only mode for active framework design, scenario development, and
RL experiment debugging.

### Release Consumption Mode

Use this mode later only after AeroEdgeRL defines a stable compatibility target.

```text
source: version-pinned package or git tag
install: locked dependency
validation: compatibility tests
```

In release mode, AeroEdgeRL should pin an exact GrADyS-SIM version or commit.
Until that compatibility contract exists, do not mix package-installed
`gradysim` with the local research checkout.

## Import Invariant

`scripts/check_environment.py` is the gatekeeper.

It checks:

- Python version;
- `aeroedge_rl` import;
- `gradysim` import;
- `DynamicVelocityMobilityConfiguration` availability;
- whether `gradysim.__file__` lives under the expected local checkout.

If this check fails, do not run experiments.

## Multi-Host Rule

Mac and Windows/WSL2 should use the same dependency model:

```text
same repo layout when possible
same conda environment name
same editable install order
same environment check
```

If the simulator checkout is not a sibling of AeroEdgeRL, set:

```bash
export AEROEDGE_GRADYSIM_ROOT=/absolute/path/to/gradys-sim-nextgen
```

Then rerun:

```bash
python scripts/check_environment.py
```

## Practical Rule

Do not rely on `PYTHONPATH` for normal development.

Use `PYTHONPATH` only as a temporary rescue tool before the editable installs
are fixed. The normal workflow is always:

```text
clean conda environment + editable local installs + environment check
```
