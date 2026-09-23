from argparse import Namespace

from aeroedge_rl.experiments.cli import rllib_ppo_smoke


def test_ppo_smoke_env_config_keeps_core_and_rllib_options():
    args = Namespace(
        num_uavs=2,
        num_devices=5,
        episode_duration=9.0,
        control_interval=1.5,
        candidate_limit=3,
        task_arrival_probability=0.2,
        deadline_range=(10.0, 20.0),
        compute_demand_range=(1.0, 2.0),
        data_size_range=(0.5, 1.5),
        seed=11,
        team_reward=True,
        action_mask=True,
        mask_hover_when_candidates=False,
    )

    config = rllib_ppo_smoke._env_config(args)

    assert config["num_uavs"] == 2
    assert config["deadline_range"] == (10.0, 20.0)
    assert config["rllib_team_reward"] is True
    assert config["rllib_action_mask"] is True
    assert config["rllib_auto_increment_seed"] is True


def test_training_summary_reads_legacy_and_env_runner_metrics():
    result = {
        "env_runners": {
            "episode_reward_mean": 3.5,
            "num_env_steps_sampled_lifetime": 128,
            "num_episodes": 4,
        },
        "training_iteration": 2,
    }

    summary = rllib_ppo_smoke._training_summary(1, result)

    assert summary["iteration"] == 1
    assert summary["episode_reward_mean"] == 3.5
    assert summary["num_episodes"] == 4
    assert summary["num_env_steps_sampled_lifetime"] == 128
    assert summary["training_iteration"] == 2
