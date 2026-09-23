import random

from aeroedge_rl.baselines.policies import BASELINE_POLICIES
from aeroedge_rl.experiments.runner import run_policy_episodes, summarize_by_policy
from aeroedge_rl.scenarios.uav_edge_service import GradysUAVServiceCoreEnv, UAVServiceEnvConfig


def test_baseline_policies_emit_valid_actions():
    env = GradysUAVServiceCoreEnv(
        UAVServiceEnvConfig(
            num_uavs=2,
            num_devices=4,
            candidate_limit=2,
            episode_duration=3.0,
            task_arrival_probability=1.0,
            seed=7,
        )
    )

    try:
        env.reset(seed=7)
        rng = random.Random(3)
        for policy in BASELINE_POLICIES.values():
            actions = policy(env, rng)
            assert set(actions) == set(env.agents)
            assert all(0 <= action < env.action_size for action in actions.values())
    finally:
        env.close()


def test_run_policy_episodes_and_summary():
    config = UAVServiceEnvConfig(
        num_uavs=1,
        num_devices=3,
        candidate_limit=2,
        episode_duration=3.0,
        task_arrival_probability=0.2,
        seed=5,
    )
    rows = run_policy_episodes(
        policy_name="hover",
        policy=BASELINE_POLICIES["hover"],
        config=config,
        episodes=1,
        seed=5,
    )
    summary = summarize_by_policy(rows)

    assert len(rows) == 1
    assert rows[0].policy == "hover"
    assert rows[0].steps > 0
    assert summary["hover"]["episodes"] == 1.0

