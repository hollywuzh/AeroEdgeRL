from argparse import Namespace

from aeroedge_rl.experiments.cli.no_rl_demo import _env_config, _json_safe


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
