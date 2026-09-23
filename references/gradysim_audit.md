# Current GrADyS Audit Notes

These notes summarize the initial reading of the existing GrADyS-SIM codebase.

## Existing Strengths

- Small and understandable discrete-event core.
- Clear protocol/provider abstraction.
- Handler mechanism for simulator capabilities.
- `step_simulation()` already supports non-blocking stepping.
- Dynamic velocity mobility is already close to RL control needs.
- The existing `showcases/rl-bridge` validates the basic RL integration idea.

## Existing RL Bridge Pattern

The current prototype follows a good pattern:

```text
GrADyS simulator
  -> dependency-light core environment
  -> Gymnasium adapter
  -> PettingZoo adapter
  -> RLlib adapter
```

This should become the formal AeroEdgeRL architecture.

## Key Gaps To Fix

- Move RL code out of `showcases/`.
- Define public action-mask and global-state APIs.
- Avoid adapter access to private fields.
- Add deterministic seed handling.
- Add exact documentation for RL control interval vs event timestamps.
- Separate scenario logic from library-specific wrappers.
- Avoid package-name confusion with installed `gradysim` versions.

## First Technical Risk

Local development can accidentally import an installed `gradysim` package
instead of the current workspace package. The new project should use a clean
virtual environment and package name (`aeroedge_rl`) to avoid this ambiguity.

