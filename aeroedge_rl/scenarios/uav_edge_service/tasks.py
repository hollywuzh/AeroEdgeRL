"""Task models for the UAV edge service scenario."""

from dataclasses import dataclass
from typing import Tuple

Position2D = Tuple[float, float]


@dataclass(frozen=True)
class Task:
    task_id: int
    device_id: int
    location: Position2D
    arrival_time: float
    deadline: float
    compute_demand: float
    data_size: float

