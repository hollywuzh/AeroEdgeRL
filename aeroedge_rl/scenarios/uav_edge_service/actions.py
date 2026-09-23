"""Action helpers for the UAV edge service scenario."""

from aeroedge_rl.rl.result import ActionMask


def build_action_mask(
    action_size: int,
    candidate_count: int,
    can_select_candidates: bool,
) -> ActionMask:
    """Build a discrete action mask.

    Action 0 is hover / keep current target. Actions 1..K select visible
    candidate tasks.
    """
    mask = [0.0] * action_size
    mask[0] = 1.0

    if not can_select_candidates:
        return mask

    for index in range(min(candidate_count, action_size - 1)):
        mask[index + 1] = 1.0
    return mask

