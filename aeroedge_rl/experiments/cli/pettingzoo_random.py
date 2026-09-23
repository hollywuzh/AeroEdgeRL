"""Minimal PettingZoo parallel random-action smoke test."""

from __future__ import annotations

from aeroedge_rl.adapters.pettingzoo_parallel_env import GradysUAVServiceParallelEnv
from aeroedge_rl.scenarios.uav_edge_service import UAVServiceEnvConfig


def main() -> None:
    config = UAVServiceEnvConfig(
        num_uavs=2,
        num_devices=5,
        episode_duration=10.0,
        control_interval=1.0,
        task_arrival_probability=0.08,
        candidate_limit=3,
        seed=5,
    )
    try:
        env = GradysUAVServiceParallelEnv(config)
    except ImportError as exc:
        raise SystemExit(str(exc)) from exc

    observations, _infos = env.reset(seed=5)
    print(
        "PettingZoo smoke test: "
        f"agents={env.agents} obs_shapes="
        f"{ {agent: observation.shape for agent, observation in observations.items()} }"
    )

    step = 0
    while env.agents:
        actions = {
            agent: env.action_space(agent).sample()
            for agent in env.agents
        }
        observations, rewards, terminations, truncations, _infos = env.step(actions)
        done = all(terminations.values()) or all(truncations.values())
        print(
            f"step={step:02d} reward_sum={sum(rewards.values()):.2f} "
            f"done={done} {env.render()}"
        )
        step += 1

    env.close()
    print("PettingZoo random-action smoke test finished.")


if __name__ == "__main__":
    main()

