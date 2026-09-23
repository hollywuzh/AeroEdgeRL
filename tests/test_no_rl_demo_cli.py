from argparse import Namespace
import json
from pathlib import Path

import pytest

from aeroedge_rl.experiments.cli.no_rl_demo import _env_config, _json_safe, main


def test_no_rl_demo_env_config_maps_cli_args():
    args = Namespace(
        num_uavs=2,
        num_devices=6,
        episode_duration=10.0,
        control_interval=0.5,
        candidate_limit=4,
        task_arrival_probability=0.25,
        deadline_range=(1.0, 2.0),
        compute_demand_range=(3.0, 4.0),
        data_size_range=(5.0, 6.0),
        seed=13,
    )

    config = _env_config(args)

    assert config.num_uavs == 2
    assert config.num_devices == 6
    assert config.control_interval == 0.5
    assert config.candidate_limit == 4
    assert config.deadline_range == (1.0, 2.0)
    assert config.seed == 13


def test_json_safe_converts_nested_item_values():
    class Scalar:
        def item(self):
            return 3

    assert _json_safe({"x": [Scalar()]}) == {"x": [3]}


def test_no_rl_trace_keeps_decision_state_and_positions(tmp_path: Path, monkeypatch):
    output = tmp_path / "trace.jsonl"
    monkeypatch.setattr(
        "sys.argv",
        [
            "no_rl_demo", "--seed", "7", "--num-uavs", "1",
            "--num-devices", "3", "--episode-duration", "3",
            "--task-arrival-probability", "1", "--output", str(output),
        ],
    )
    main()
    records = [json.loads(line) for line in output.read_text().splitlines()]
    assert records
    assert records[0]["actions"]["uav_0"] >= 0
    assert records[0]["action_masks"]["uav_0"][records[0]["actions"]["uav_0"]]
    assert records[0]["candidate_task_ids"]["uav_0"]
    assert records[0]["agent_positions_before"]["uav_0"] == [50.0, 50.0, 30.0]
    assert all(row["time"] >= row["time_before"] for row in records)


def test_trajectory_plot_from_trace(tmp_path: Path, monkeypatch):
    pytest.importorskip("matplotlib")
    output = tmp_path / "trace.jsonl"
    plot = tmp_path / "trajectory.png"
    monkeypatch.setattr(
        "sys.argv",
        [
            "no_rl_demo", "--seed", "7", "--num-uavs", "1",
            "--num-devices", "3", "--episode-duration", "3",
            "--task-arrival-probability", "1", "--output", str(output),
            "--plot-output", str(plot),
        ],
    )
    main()
    assert plot.is_file()
    assert plot.stat().st_size > 1000
