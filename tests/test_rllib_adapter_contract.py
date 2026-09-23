import importlib.util
import inspect

import pytest

from aeroedge_rl.adapters.rllib_multiagent_env import GradysUAVServiceRLlibEnv


def test_rllib_adapter_requires_optional_dependency_when_missing():
    if importlib.util.find_spec("ray") is not None:
        pytest.skip("RLlib is installed in this environment.")

    with pytest.raises(ImportError, match="Install RLlib support"):
        GradysUAVServiceRLlibEnv()


def test_rllib_action_mask_uses_public_core_api():
    source = inspect.getsource(GradysUAVServiceRLlibEnv._action_mask_for)

    assert "self.core.action_mask(agent)" in source
    assert "_busy_until" not in source
    assert "_targets" not in source
    assert "_tasks" not in source


def test_rllib_adapter_reset_and_step_when_installed():
    pytest.importorskip("ray.rllib")

    env = GradysUAVServiceRLlibEnv(
        {
            "num_uavs": 2,
            "num_devices": 3,
            "episode_duration": 3.0,
            "control_interval": 1.0,
            "task_arrival_probability": 0.2,
            "candidate_limit": 2,
            "seed": 3,
            "rllib_action_mask": True,
        }
    )

    try:
        observations, infos = env.reset(seed=5)
        assert set(observations) == set(env.possible_agents)
        assert set(infos) == set(env.possible_agents)

        actions = {
            agent: env.action_space.sample()
            for agent in observations
        }
        next_observations, rewards, terminateds, truncateds, step_infos = env.step(actions)

        assert set(next_observations) == set(env.possible_agents)
        assert set(rewards) == set(env.possible_agents)
        assert terminateds["__all__"] in {True, False}
        assert truncateds["__all__"] in {True, False}
        assert set(step_infos) == set(env.possible_agents)
    finally:
        env.close()

