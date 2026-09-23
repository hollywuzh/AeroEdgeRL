import pytest

from aeroedge_rl.rl.result import StepResult
from aeroedge_rl.scenarios.uav_edge_service import (
    GradysUAVServiceCoreEnv,
    UAVServiceEnvConfig,
)


def test_uav_edge_service_core_reset_and_step():
    env = GradysUAVServiceCoreEnv(
        UAVServiceEnvConfig(
            num_uavs=2,
            num_devices=4,
            episode_duration=3.0,
            control_interval=1.0,
            task_arrival_probability=0.2,
            seed=3,
        )
    )

    try:
        observations = env.reset(seed=5)
        assert set(observations) == {"uav_0", "uav_1"}
        assert all(len(observation) == env.observation_size for observation in observations.values())

        result = env.step({"uav_0": 0, "uav_1": 0})

        assert isinstance(result, StepResult)
        assert set(result.observations) == {"uav_0", "uav_1"}
        assert set(result.rewards) == {"uav_0", "uav_1"}
        assert set(result.infos) == {"uav_0", "uav_1"}
        assert env.time > 0.0
    finally:
        env.close()


def test_action_mask_reflects_visible_candidates():
    env = GradysUAVServiceCoreEnv(
        UAVServiceEnvConfig(
            num_uavs=1,
            num_devices=3,
            candidate_limit=2,
            episode_duration=3.0,
            task_arrival_probability=1.0,
            seed=7,
        )
    )

    try:
        env.reset(seed=9)
        candidates = env.candidate_tasks("uav_0")
        mask = env.action_mask("uav_0")

        assert len(mask) == env.action_size
        assert mask[0] == 1.0
        assert mask[1:] == [1.0] * len(candidates)
        assert sum(mask) == 1.0 + len(candidates)
    finally:
        env.close()


def test_action_mask_rejects_unknown_agent():
    env = GradysUAVServiceCoreEnv(UAVServiceEnvConfig(num_uavs=1, num_devices=1, seed=1))

    try:
        env.reset(seed=1)
        with pytest.raises(KeyError):
            env.action_mask("missing_uav")
    finally:
        env.close()


def test_global_state_is_concatenated_agent_observation_vector():
    env = GradysUAVServiceCoreEnv(
        UAVServiceEnvConfig(
            num_uavs=2,
            num_devices=3,
            candidate_limit=2,
            episode_duration=3.0,
            task_arrival_probability=0.5,
            seed=11,
        )
    )

    try:
        env.reset(seed=13)
        state = env.global_state()

        assert len(state) == env.observation_size * len(env.agents)
        assert all(isinstance(value, float) for value in state)
    finally:
        env.close()


def test_state_queries_require_reset():
    env = GradysUAVServiceCoreEnv(UAVServiceEnvConfig(num_uavs=1, num_devices=1, seed=1))

    with pytest.raises(RuntimeError):
        env.action_mask("uav_0")

    with pytest.raises(RuntimeError):
        env.global_state()
