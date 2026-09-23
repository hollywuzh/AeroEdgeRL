"""Minimal RLlib PPO smoke training for the UAV edge service scenario."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from aeroedge_rl.adapters.rllib_action_mask_model import (
    ACTION_MASK_MODEL,
    register_action_mask_model,
)
from aeroedge_rl.adapters.rllib_multiagent_env import GradysUAVServiceRLlibEnv


ENV_NAME = "aeroedge_uav_service_rllib_ppo_smoke"
POLICY_ID = "shared_uav_policy"


def main() -> None:
    args = _parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        ray, PPOConfig, PolicySpec, register_env = _require_rllib()
        env_config = _env_config(args)
        register_env(ENV_NAME, lambda config: GradysUAVServiceRLlibEnv(dict(config)))
        if args.action_mask:
            register_action_mask_model()

        reference_env = GradysUAVServiceRLlibEnv(env_config)
        try:
            observation_space = reference_env.observation_space
            action_space = reference_env.action_space
        finally:
            reference_env.close()
    except ImportError as exc:
        raise SystemExit(str(exc)) from exc

    ray.init(
        local_mode=args.local_mode,
        include_dashboard=False,
        ignore_reinit_error=True,
        num_cpus=args.num_cpus,
        log_to_driver=not args.quiet,
    )

    algorithm = None
    results: list[dict[str, Any]] = []
    try:
        config = _ppo_config(
            PPOConfig=PPOConfig,
            PolicySpec=PolicySpec,
            args=args,
            env_config=env_config,
            observation_space=observation_space,
            action_space=action_space,
        )
        algorithm = config.build_algo()

        for iteration in range(args.iterations):
            result = algorithm.train()
            summary = _training_summary(iteration, result)
            results.append(summary)
            print(
                f"iter={iteration:03d} "
                f"reward_mean={_fmt(summary['episode_reward_mean'])} "
                f"episodes={_fmt(summary['num_episodes'])} "
                f"env_steps={_fmt(summary['num_env_steps_sampled_lifetime'])}"
            )

        checkpoint = None
        if args.checkpoint:
            checkpoint_dir = Path(args.checkpoint_dir)
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
            checkpoint = str(algorithm.save(checkpoint_dir))
            print(f"Wrote RLlib checkpoint: {checkpoint}")
    finally:
        if algorithm is not None:
            algorithm.stop()
        ray.shutdown()

    payload = {
        "ray_version": ray.__version__,
        "env_name": ENV_NAME,
        "policy_id": POLICY_ID,
        "env_config": env_config,
        "ppo_config": {
            "api_stack": "legacy",
            "action_mask": args.action_mask,
            "team_reward": args.team_reward,
            "train_batch_size": args.train_batch_size,
            "minibatch_size": args.minibatch_size,
            "num_epochs": args.num_epochs,
            "rollout_fragment_length": args.rollout_fragment_length,
            "iterations": args.iterations,
            "lr": args.lr,
            "gamma": args.gamma,
            "lambda": args.lambda_,
        },
        "checkpoint": checkpoint,
        "results": results,
    }
    output_path.write_text(json.dumps(_json_safe(payload), indent=2) + "\n")
    print(f"Wrote PPO smoke metrics: {output_path.resolve()}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--num-uavs", type=int, default=2)
    parser.add_argument("--num-devices", type=int, default=8)
    parser.add_argument("--episode-duration", type=float, default=12.0)
    parser.add_argument("--control-interval", type=float, default=1.0)
    parser.add_argument("--candidate-limit", type=int, default=3)
    parser.add_argument("--task-arrival-probability", type=float, default=0.08)
    parser.add_argument("--deadline-range", type=float, nargs=2, default=(20.0, 60.0))
    parser.add_argument("--compute-demand-range", type=float, nargs=2, default=(20.0, 200.0))
    parser.add_argument("--data-size-range", type=float, nargs=2, default=(0.5, 8.0))
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--train-batch-size", type=int, default=64)
    parser.add_argument("--minibatch-size", type=int, default=32)
    parser.add_argument("--num-epochs", type=int, default=1)
    parser.add_argument("--rollout-fragment-length", type=int, default=16)
    parser.add_argument("--lr", type=float, default=5e-4)
    parser.add_argument("--gamma", type=float, default=0.99)
    parser.add_argument("--lambda", dest="lambda_", type=float, default=0.95)
    parser.add_argument("--num-cpus", type=int, default=1)
    parser.add_argument("--local-mode", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--checkpoint", action="store_true")
    parser.add_argument("--checkpoint-dir", default="outputs/rllib_checkpoints")
    parser.add_argument("--team-reward", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--action-mask", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument(
        "--mask-hover-when-candidates",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument("--output", default="outputs/rllib_ppo_smoke_metrics.json")
    return parser.parse_args()


def _env_config(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "num_uavs": args.num_uavs,
        "num_devices": args.num_devices,
        "episode_duration": args.episode_duration,
        "control_interval": args.control_interval,
        "candidate_limit": args.candidate_limit,
        "task_arrival_probability": args.task_arrival_probability,
        "deadline_range": tuple(args.deadline_range),
        "compute_demand_range": tuple(args.compute_demand_range),
        "data_size_range": tuple(args.data_size_range),
        "seed": args.seed,
        "rllib_team_reward": args.team_reward,
        "rllib_auto_increment_seed": True,
        "rllib_action_mask": args.action_mask,
        "rllib_mask_hover_when_candidates": args.mask_hover_when_candidates,
    }


def _ppo_config(
    PPOConfig,
    PolicySpec,
    args: argparse.Namespace,
    env_config: dict[str, Any],
    observation_space,
    action_space,
):
    model_config: dict[str, Any] = {
        "fcnet_hiddens": [64, 64],
        "fcnet_activation": "tanh",
    }
    if args.action_mask:
        model_config["custom_model"] = ACTION_MASK_MODEL

    return (
        PPOConfig()
        .api_stack(
            enable_env_runner_and_connector_v2=False,
            enable_rl_module_and_learner=False,
        )
        .environment(
            env=ENV_NAME,
            env_config=env_config,
            disable_env_checking=False,
        )
        .framework("torch")
        .resources(num_gpus=0)
        .env_runners(
            num_env_runners=0,
            rollout_fragment_length=args.rollout_fragment_length,
            batch_mode="complete_episodes",
        )
        .training(
            train_batch_size=args.train_batch_size,
            minibatch_size=args.minibatch_size,
            num_epochs=args.num_epochs,
            lr=args.lr,
            gamma=args.gamma,
            lambda_=args.lambda_,
            model=model_config,
        )
        .multi_agent(
            policies={
                POLICY_ID: PolicySpec(
                    policy_class=None,
                    observation_space=observation_space,
                    action_space=action_space,
                    config={},
                )
            },
            policy_mapping_fn=lambda agent_id, *args, **kwargs: POLICY_ID,
        )
    )


def _training_summary(iteration: int, result: dict[str, Any]) -> dict[str, Any]:
    env_runners = result.get("env_runners", {})
    return {
        "iteration": iteration,
        "episode_reward_mean": _first_present(result, env_runners, "episode_reward_mean"),
        "episode_reward_min": _first_present(result, env_runners, "episode_reward_min"),
        "episode_reward_max": _first_present(result, env_runners, "episode_reward_max"),
        "episode_len_mean": _first_present(result, env_runners, "episode_len_mean"),
        "num_episodes": _first_present(result, env_runners, "num_episodes", "episodes_this_iter"),
        "num_env_steps_sampled_lifetime": _first_present(
            result,
            env_runners,
            "num_env_steps_sampled_lifetime",
            "num_env_steps_sampled",
        ),
        "timesteps_total": result.get("timesteps_total"),
        "training_iteration": result.get("training_iteration"),
        "time_total_s": result.get("time_total_s"),
    }


def _first_present(primary: dict[str, Any], secondary: dict[str, Any], *keys: str):
    for key in keys:
        if key in primary:
            return primary[key]
        if key in secondary:
            return secondary[key]
    return None


def _require_rllib():
    os.environ.setdefault("RAY_DEDUP_LOGS", "0")
    os.environ.setdefault("PYTHONWARNINGS", "ignore::DeprecationWarning")
    try:
        import ray
        from ray.rllib.algorithms.ppo import PPOConfig
        from ray.rllib.policy.policy import PolicySpec
        from ray.tune.registry import register_env
    except ImportError as exc:  # pragma: no cover - optional dependency path
        raise ImportError(
            "Install RLlib support with `python -m pip install 'ray[rllib]' torch` "
            "to run PPO smoke training."
        ) from exc
    return ray, PPOConfig, PolicySpec, register_env


def _json_safe(value):
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if hasattr(value, "item"):
        return value.item()
    return value


def _fmt(value) -> str:
    if value is None:
        return "None"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


if __name__ == "__main__":
    main()
