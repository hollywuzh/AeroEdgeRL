"""Plot control-boundary UAV trajectories from no-RL trace records."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def plot_trajectory(
    records: Sequence[Mapping[str, Any]],
    output_path: str,
    *,
    area_size: float,
) -> None:
    """Show each UAV in its own panel to keep path crossings interpretable."""
    if not records:
        raise ValueError("At least one trace record is required for plotting.")

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    from matplotlib.colors import Normalize

    agents = sorted(records[0]["agent_positions"])
    devices = records[0]["device_positions"]
    figure, axes = plt.subplots(
        1, len(agents), figsize=(5.6 * len(agents), 5.4), squeeze=False,
        constrained_layout=True,
    )
    times = [float(records[0]["time_before"])] + [float(row["time"]) for row in records]
    normalizer = Normalize(vmin=times[0], vmax=max(times[-1], times[0] + 1e-9))

    for agent, ax in zip(agents, axes[0]):
        positions = [records[0]["agent_positions_before"][agent]] + [
            row["agent_positions"][agent] for row in records
        ]
        points = [(float(position[0]), float(position[1])) for position in positions]
        segments = list(zip(points[:-1], points[1:]))
        if devices:
            ax.scatter(
                [point[0] for point in devices],
                [point[1] for point in devices],
                s=16, color="#87939c", alpha=0.65, label="Ground device", zorder=2,
            )
        line = LineCollection(
            segments, cmap="viridis", norm=normalizer, linewidth=2.5,
            capstyle="round", zorder=3,
        )
        line.set_array(times[1:])
        ax.add_collection(line)
        ax.scatter(*points[0], s=85, marker="o", color="#136f63", edgecolor="white",
                   linewidth=0.9, label="Start", zorder=4)
        ax.scatter(*points[-1], s=85, marker="X", color="#d45113", edgecolor="white",
                   linewidth=0.9, label="End", zorder=4)
        ax.set(xlim=(0, area_size), ylim=(0, area_size), xlabel="x (m)", ylabel="y (m)")
        ax.set_aspect("equal", adjustable="box")
        ax.set_title(f"{agent} | {records[0]['policy']}")
        ax.grid(color="#d6dce0", linewidth=0.5)
        ax.legend(loc="upper right", fontsize=8, framealpha=0.9)

    figure.colorbar(line, ax=list(axes[0]), label="Simulated time (s)", shrink=0.8)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=160)
    plt.close(figure)
