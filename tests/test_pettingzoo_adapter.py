import importlib.util

import pytest

from aeroedge_rl.adapters.pettingzoo_parallel_env import GradysUAVServiceParallelEnv
from aeroedge_rl.scenarios.uav_edge_service import UAVServiceEnvConfig


def test_pettingzoo_adapter_requires_optional_dependency_when_missing():
    if importlib.util.find_spec("pettingzoo") is not None:
        pytest.skip("PettingZoo is installed in this environment.")

    with pytest.raises(ImportError, match="Install PettingZoo support"):
        GradysUAVServiceParallelEnv()


def test_pettingzoo_adapter_reset_and_step_when_installed():
    pytest.importorskip("pettingzoo")

    env = GradysUAVServiceParallelEnv(
        UAVServiceEnvConfig(
            num_uavs=2,
            num_devices=3,
            episode_duration=3.0,
            control_interval=1.0,
            task_arrival_probability=0.2,
            candidate_limit=2,
            seed=3,
        )
    )

    try:
        observations, infos = env.reset(seed=5)
        assert set(observations) == set(env.possible_agents)
        assert set(infos) == set(env.possible_agents)

        actions = {
            agent: env.action_space(agent).sample()
            for agent in env.agents
        }
        next_observations, rewards, terminations, truncations, step_infos = env.step(actions)

        assert set(next_observations) == set(env.possible_agents)
        assert set(rewards) == set(env.possible_agents)
        assert set(terminations) == set(env.possible_agents)
        assert set(truncations) == set(env.possible_agents)
        assert set(step_infos) == set(env.possible_agents)
    finally:
        env.close()

