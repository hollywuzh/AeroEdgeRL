"""Run an externally installed LKH executable on a small Euclidean TSP."""

from __future__ import annotations

import math
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Sequence


def solve_lkh(
    points: Sequence[tuple[float, float]],
    *,
    binary: str | os.PathLike[str] | None = None,
    seed: int = 7,
    scale: int = 1000,
    timeout: float = 30.0,
) -> tuple[list[int], float]:
    """Return a depot-first closed tour and its unrounded Euclidean length.

    Point 0 is the depot. The returned route includes the terminal depot.
    LKH optimizes rounded integer weights, so its objective may differ slightly
    from the reported continuous Euclidean length.
    """
    if len(points) < 3:
        raise ValueError("LKH requires at least three points including the depot")
    if scale <= 0 or timeout <= 0 or seed < 0:
        raise ValueError("scale and timeout must be positive; seed must be nonnegative")
    if any(len(point) != 2 or not all(math.isfinite(x) for x in point) for point in points):
        raise ValueError("all points must contain two finite coordinates")

    executable = str(binary or os.environ.get("AEROEDGE_LKH_BINARY") or "LKH")
    resolved = shutil.which(executable)
    if resolved is None:
        raise FileNotFoundError(
            f"LKH executable not found: {executable}; set AEROEDGE_LKH_BINARY"
        )

    size = len(points)
    weights = [
        [round(scale * math.dist(left, right)) if i != j else 0
         for j, right in enumerate(points)]
        for i, left in enumerate(points)
    ]
    if any(i != j and weights[i][j] == 0 for i in range(size) for j in range(size)):
        raise ValueError("scale is too small to represent all nonzero distances")

    with tempfile.TemporaryDirectory(prefix="aeroedge-lkh-") as directory:
        root = Path(directory)
        problem = root / "instance.tsp"
        tour = root / "result.tour"
        parameters = root / "run.par"
        problem.write_text(
            "NAME : aeroedge\nTYPE : TSP\nDIMENSION : " + str(size)
            + "\nEDGE_WEIGHT_TYPE : EXPLICIT\nEDGE_WEIGHT_FORMAT : FULL_MATRIX\n"
            + "EDGE_WEIGHT_SECTION\n"
            + "\n".join(" ".join(map(str, row)) for row in weights)
            + "\nEOF\n",
            encoding="ascii",
        )
        parameters.write_text(
            f"PROBLEM_FILE = {problem}\nTOUR_FILE = {tour}\n"
            f"RUNS = 1\nSEED = {seed}\nTRACE_LEVEL = 0\n",
            encoding="ascii",
        )
        result = subprocess.run(
            [resolved, str(parameters)], capture_output=True, text=True,
            timeout=timeout, check=False,
        )
        if result.returncode or not tour.is_file():
            raise RuntimeError(
                f"LKH failed (exit {result.returncode}): "
                f"{(result.stderr or result.stdout)[-1000:]}"
            )
        lines = tour.read_text(encoding="ascii").splitlines()

    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == "TOUR_SECTION")
        node_ids = []
        for line in lines[start + 1:]:
            value = int(line.strip())
            if value == -1:
                break
            node_ids.append(value - 1)
    except (StopIteration, ValueError) as exc:
        raise RuntimeError("LKH returned a malformed tour") from exc
    if len(node_ids) != size or set(node_ids) != set(range(size)):
        raise RuntimeError("LKH returned a duplicate, missing, or invalid node")
    depot_index = node_ids.index(0)
    route = node_ids[depot_index:] + node_ids[:depot_index] + [0]
    distance = sum(math.dist(points[a], points[b]) for a, b in zip(route, route[1:]))
    return route, distance
