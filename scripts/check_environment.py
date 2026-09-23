"""Validate the active AeroEdgeRL development environment.

This script catches the most common Phase 1 setup mistake: importing an older
installed `gradysim` package instead of the local GrADyS-SIM workspace.
"""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path


def main() -> int:
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version.split()[0]}")

    if sys.version_info < (3, 10):
        print("ERROR: AeroEdgeRL requires Python >= 3.10.")
        return 1

    try:
        import aeroedge_rl
        import gradysim
    except ImportError as exc:
        print(f"ERROR: Could not import required package: {exc}")
        return 1

    gradysim_path = Path(gradysim.__file__).resolve()
    print(f"aeroedge_rl version: {aeroedge_rl.__version__}")
    print(f"gradysim path: {gradysim_path}")

    mobility_module = importlib.import_module("gradysim.simulator.handler.mobility")
    mobility_path = Path(mobility_module.__file__).resolve()
    print(f"gradysim mobility path: {mobility_path}")

    if not hasattr(mobility_module, "DynamicVelocityMobilityConfiguration"):
        print("ERROR: Imported gradysim does not expose DynamicVelocityMobilityConfiguration.")
        print("This usually means an older installed gradysim package is being imported.")
        return 1

    expected_root = _expected_gradysim_root()
    if expected_root is not None:
        expected_package_dir = (expected_root / "gradysim").resolve()
        if not _is_relative_to(gradysim_path, expected_package_dir):
            print(f"ERROR: gradysim is not imported from expected local workspace: {expected_root}")
            print("Install the local simulator into this environment:")
            print(f"  python -m pip install -e {expected_root}")
            return 1
        print(f"Expected gradysim root: {expected_root}")
    else:
        print("Expected gradysim root: not checked")

    print("Environment check passed.")
    return 0


def _expected_gradysim_root() -> Path | None:
    configured = os.environ.get("AEROEDGE_GRADYSIM_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()

    project_root = Path(__file__).resolve().parents[1]
    sibling = project_root.parent / "gradys-sim-nextgen"
    if sibling.exists():
        return sibling.resolve()
    return None


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


if __name__ == "__main__":
    raise SystemExit(main())

