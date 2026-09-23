"""Configuration for the UAV edge service scenario."""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class UAVServiceEnvConfig:
    num_uavs: int = 4
    num_devices: int = 30
    area_size: float = 100.0
    altitude: float = 30.0
    episode_duration: float = 120.0
    control_interval: float = 1.0
    mobility_update_rate: float = 0.2
    max_speed_xy: float = 12.0
    max_speed_z: float = 4.0
    max_acc_xy: float = 8.0
    max_acc_z: float = 4.0
    candidate_limit: int = 5
    service_radius: float = 2.0
    compute_rate: float = 50.0
    task_arrival_probability: float = 0.08
    deadline_range: Tuple[float, float] = (20.0, 60.0)
    compute_demand_range: Tuple[float, float] = (20.0, 200.0)
    data_size_range: Tuple[float, float] = (0.5, 8.0)
    workload_mode: str = "synthetic"
    alibaba_task_table_path: Optional[str] = None
    alibaba_max_rows: int = 50000
    success_reward: float = 10.0
    miss_penalty: float = -10.0
    movement_penalty: float = -0.01
    wait_penalty: float = -0.02
    seed: Optional[int] = None

