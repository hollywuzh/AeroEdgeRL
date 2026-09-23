import importlib.util

import pytest

from aeroedge_rl.adapters.gymnasium_env import GradysUAVServiceGymEnv
from aeroedge_rl.scenarios.uav_edge_service import UAVServiceEnvConfig


def test_gymnasium_adapter_requires_optional_dependency_when_missing():
    if importlib.util.find_spec("gymnasium") is not None:
        pytest.skip("Gymnasium is installed in this environment.")

    with pytest.raises(ImportError, match="Install Gymnasium support"):
        GradysUAVServiceGymEnv()


def test_gymnasium_adapter_reset_and_step_when_installed():
    pytest.importorskip("gymnasium")

    env = GradysUAVServiceGymEnv(
        UAVServiceEnvConfig(
            num_uavs=1,
            num_devices=3,
            episode_duration=3.0,
            control_interval=1.0,
            task_arrival_probability=0.2,
            candidate_limit=2,
            seed=3,
        )
    )

    try:
        observation, info = env.reset(seed=5)
        assert observation.shape == env.observation_space.shape
        assert info == {}

        action = env.action_space.sample()
        next_observation, reward, terminated, truncated, step_info = env.step(action)

        assert next_observation.shape == env.observation_space.shape
        assert isinstance(reward, float)
        assert isinstance(terminated, bool)
        assert isinstance(truncated, bool)
        assert "agent_infos" in step_info
    finally:
        env.close()

