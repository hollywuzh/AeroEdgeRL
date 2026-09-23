from aeroedge_rl import __version__
from aeroedge_rl.rl.result import StepResult


def test_package_import_is_lightweight():
    assert __version__ == "0.1.0"


def test_step_result_shape():
    result = StepResult(
        observations={"uav_0": [0.0]},
        rewards={"uav_0": 0.0},
        terminated=False,
        truncated=False,
        infos={"uav_0": {}},
    )

    assert result.observations["uav_0"] == [0.0]
    assert result.rewards["uav_0"] == 0.0
    assert not result.terminated
    assert not result.truncated

