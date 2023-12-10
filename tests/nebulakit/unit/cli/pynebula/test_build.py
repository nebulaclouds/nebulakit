import os

from click.testing import CliRunner

from nebulakit.clis.sdk_in_container import pynebula
from nebulakit.image_spec.image_spec import ImageBuildEngine

WORKFLOW_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "image_spec_wf.py")


def test_build(mock_image_spec_builder):
    ImageBuildEngine.register("test", mock_image_spec_builder)
    runner = CliRunner()
    result = runner.invoke(pynebula.main, ["build", "--fast", WORKFLOW_FILE, "wf"])
    assert result.exit_code == 0

    result = runner.invoke(pynebula.main, ["build", WORKFLOW_FILE, "wf"])
    assert result.exit_code == 0

    result = runner.invoke(pynebula.main, ["build", WORKFLOW_FILE, "wf"])
    assert result.exit_code == 0

    result = runner.invoke(pynebula.main, ["build", "--help"])
    assert result.exit_code == 0

    result = runner.invoke(pynebula.main, ["build", "../", "wf"])
    assert result.exit_code == 1
