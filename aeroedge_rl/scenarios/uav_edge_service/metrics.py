"""Metrics helpers for the UAV edge service scenario."""

from typing import Dict


def build_metrics_snapshot(
    *,
    time: float,
    generated_tasks: int,
    pending_tasks: int,
    hits: int,
    misses: int,
    total_energy_used: float,
    num_agents: int,
) -> Dict[str, float]:
    completed_or_missed = hits + misses
    success_rate = hits / completed_or_missed if completed_or_missed else 0.0
    miss_rate = misses / completed_or_missed if completed_or_missed else 0.0
    return {
        "time": time,
        "generated_tasks": float(generated_tasks),
        "pending_tasks": float(pending_tasks),
        "hits": float(hits),
        "misses": float(misses),
        "completed_or_missed_tasks": float(completed_or_missed),
        "success_rate": success_rate,
        "miss_rate": miss_rate,
        "total_energy_used": total_energy_used,
        "mean_energy_used": total_energy_used / max(1, num_agents),
    }

