"""Shared environment result structures."""

from dataclasses import dataclass
from typing import Any

AgentId = str
Observation = list[float]
Action = int
ActionMask = list[float]


@dataclass
class StepResult:
    """Backend-independent multi-agent environment step result."""

    observations: dict[AgentId, Observation]
    rewards: dict[AgentId, float]
    terminated: bool
    truncated: bool
    infos: dict[AgentId, dict[str, Any]]
