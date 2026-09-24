import math
import os
from pathlib import Path

import pytest

from aeroedge_rl.baselines.lkh import solve_lkh


POINTS = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]


def test_lkh_requires_an_executable():
    with pytest.raises(FileNotFoundError, match="AEROEDGE_LKH_BINARY"):
        solve_lkh(POINTS, binary="/nonexistent/aeroedge/LKH")


def test_lkh_rejects_invalid_points():
    with pytest.raises(ValueError, match="finite"):
        solve_lkh([(0.0, 0.0), (math.nan, 0.0), (1.0, 1.0)])


def test_lkh_local_integration():
    binary = Path(os.environ.get("AEROEDGE_LKH_BINARY", ""))
    if not binary.is_file():
        pytest.skip("Set AEROEDGE_LKH_BINARY for the local integration test")
    route, distance = solve_lkh(POINTS, binary=binary)
    assert route[0] == route[-1] == 0
    assert set(route[:-1]) == set(range(len(POINTS)))
    assert distance == pytest.approx(4.0)
