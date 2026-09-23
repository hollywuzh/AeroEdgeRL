import importlib.util

import pytest

from aeroedge_rl.adapters.rllib_action_mask_model import (
    ACTION_MASK_MODEL,
    AeroEdgeActionMaskTorchModel,
    register_action_mask_model,
)


def test_action_mask_model_name_is_aeroedge_specific():
    assert ACTION_MASK_MODEL == "aeroedge_action_mask_model"


def test_action_mask_model_requires_optional_dependency_when_missing():
    if importlib.util.find_spec("ray") is not None:
        pytest.skip("RLlib is installed in this environment.")

    with pytest.raises(ImportError, match="Install RLlib support"):
        register_action_mask_model()


def test_action_mask_model_class_is_importable_without_rllib():
    assert AeroEdgeActionMaskTorchModel.__name__ == "AeroEdgeActionMaskTorchModel"

