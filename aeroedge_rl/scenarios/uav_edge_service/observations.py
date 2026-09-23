"""Observation helpers for the UAV edge service scenario."""

import math
from typing import List

from aeroedge_rl.scenarios.uav_edge_service.tasks import Task


def observation_size(candidate_limit: int) -> int:
    # x, y, energy, busy remaining, queue length
    # plus K candidates: dx, dy, distance, deadline slack,
    # estimated service slack, compute demand, data size.
    return 5 + 7 * candidate_limit


def build_agent_observation(
    *,
    x_pos: float,
    y_pos: float,
    time: float,
    energy_used: float,
    busy_until: float,
    pending_task_count: int,
    num_devices: int,
    candidates: List[Task],
    candidate_limit: int,
    area_size: float,
    episode_duration: float,
    max_speed_xy: float,
    compute_rate: float,
    compute_observation_scale: float,
    data_observation_scale: float,
) -> List[float]:
    obs = [
        x_pos / area_size,
        y_pos / area_size,
        energy_used / 1000.0,
        max(0.0, busy_until - time) / episode_duration,
        pending_task_count / max(1, num_devices),
    ]

    for task in candidates[:candidate_limit]:
        distance = _distance_2d((x_pos, y_pos), task.location)
        travel_time = distance / max(max_speed_xy, 1e-9)
        service_time = task.compute_demand / max(compute_rate, 1e-9)
        obs.extend(
            [
                (task.location[0] - x_pos) / area_size,
                (task.location[1] - y_pos) / area_size,
                distance / area_size,
                (task.deadline - time) / episode_duration,
                (task.deadline - time - travel_time - service_time)
                / episode_duration,
                task.compute_demand / compute_observation_scale,
                task.data_size / data_observation_scale,
            ]
        )

    for _ in range(candidate_limit - min(len(candidates), candidate_limit)):
        obs.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    return obs


def _distance_2d(start, end) -> float:
    return math.hypot(end[0] - start[0], end[1] - start[1])

