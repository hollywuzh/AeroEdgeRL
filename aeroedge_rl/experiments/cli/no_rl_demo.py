"""Trace a no-RL rule-based policy in the UAV edge service simulator."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

from aeroedge_rl.baselines.policies import BASELINE_POLICIES
from aeroedge_rl.scenarios.uav_edge_service import UAVServiceEnvConfig
from aeroedge_rl.scenarios.uav_edge_service.environment import GradysUAVServiceCoreEnv


def main() -> None:
    args = _parse_args()
    policy = BASELINE_POLICIES[args.policy]
    rng = random.Random(args.seed + 100003)
    env = GradysUAVServiceCoreEnv(_env_config(args))
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, Any]] = []
    observations = env.reset(seed=args.seed)
    print(
        "No-RL demo: "
        f"policy={args.policy} agents={env.agents} "
        f"obs_size={env.observation_size} action_size={env.action_size}"
    )

    try:
        done = False
        step = 0
        while not done and step < args.max_steps:
            actions = policy(env, rng)
            result = env.step(actions)
            metrics = env.metrics_snapshot()
            record = {
                "step": step,
                "time": env.time,
                "policy": args.policy,
                "actions": actions,
                "action_masks": {agent: env.action_mask(agent) for agent in env.agents},
                "reward_sum": float(sum(result.rewards.values())),
                "rewards": result.rewards,
                "metrics": metrics,
                "render_text": env.render_text(),
                "candidate_task_ids": {
                    agent: [task.task_id for task in env.candidate_tasks(agent)]
                    for agent in env.agents
                },
                "observation_sizes": {
                    agent: len(observation)
                    for agent, observation in observations.items()
                },
            }
            records.append(record)
            print(
                f"step={step:02d} "
                f"t={record['time']:.1f}s "
                f"actions={actions} "
                f"reward_sum={record['reward_sum']:.2f} "
                f"pending={metrics['pending_tasks']:.0f} "
                f"hits={metrics['hits']:.0f} "
                f"misses={metrics['misses']:.0f}"
            )
            observations = result.observations
            done = result.terminated or result.truncated
            step += 1
    finally:
        env.close()

    with output_path.open("w") as file_obj:
        for record in records:
            file_obj.write(json.dumps(_json_safe(record)) + "\n")

    final_metrics = records[-1]["metrics"] if records else env.metrics_snapshot()
    print(
        "No-RL demo finished: "
        f"steps={len(records)} "
        f"hits={final_metrics['hits']:.0f} "
        f"misses={final_metrics['misses']:.0f} "
        f"pending={final_metrics['pending_tasks']:.0f}"
    )
    print(f"Wrote trace JSONL: {output_path.resolve()}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", choices=sorted(BASELINE_POLICIES), default="nearest")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--num-uavs", type=int, default=1)
    parser.add_argument("--num-devices", type=int, default=5)
    parser.add_argument("--episode-duration", type=float, default=12.0)
    parser.add_argument("--control-interval", type=float, default=1.0)
    parser.add_argument("--candidate-limit", type=int, default=3)
    parser.add_argument("--task-arrival-probability", type=float, default=0.12)
    parser.add_argument("--deadline-range", type=float, nargs=2, default=(12.0, 30.0))
    parser.add_argument("--compute-demand-range", type=float, nargs=2, default=(10.0, 80.0))
    parser.add_argument("--data-size-range", type=float, nargs=2, default=(0.5, 4.0))
    parser.add_argument("--max-steps", type=int, default=32)
    parser.add_argument("--output", default="outputs/no_rl_demo_trace.jsonl")
    return parser.parse_args()


def _env_config(args: argparse.Namespace) -> UAVServiceEnvConfig:
    return UAVServiceEnvConfig(
        num_uavs=args.num_uavs,
        num_devices=args.num_devices,
        episode_duration=args.episode_duration,
        control_interval=args.control_interval,
        candidate_limit=args.candidate_limit,
        task_arrival_probability=args.task_arrival_probability,
        deadline_range=tuple(args.deadline_range),
        compute_demand_range=tuple(args.compute_demand_range),
        data_size_range=tuple(args.data_size_range),
        seed=args.seed,
    )


def _json_safe(value):
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if hasattr(value, "item"):
        return value.item()
    return value


if __name__ == "__main__":
    main()
