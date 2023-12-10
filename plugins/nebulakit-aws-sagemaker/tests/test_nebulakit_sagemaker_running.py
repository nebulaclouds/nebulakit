import os
import sys
from unittest import mock

from scripts.nebulakit_sagemaker_runner import run as _nebula_sagemaker_run

cmd = []
cmd.extend(["--__NEBULA_ENV_VAR_env1__", "val1"])
cmd.extend(["--__NEBULA_ENV_VAR_env2__", "val2"])
cmd.extend(["--__NEBULA_CMD_0_service_venv__", "__NEBULA_CMD_DUMMY_VALUE__"])
cmd.extend(["--__NEBULA_CMD_1_pynebula-execute__", "__NEBULA_CMD_DUMMY_VALUE__"])
cmd.extend(["--__NEBULA_CMD_2_--task-module__", "__NEBULA_CMD_DUMMY_VALUE__"])
cmd.extend(["--__NEBULA_CMD_3_blah__", "__NEBULA_CMD_DUMMY_VALUE__"])
cmd.extend(["--__NEBULA_CMD_4_--task-name__", "__NEBULA_CMD_DUMMY_VALUE__"])
cmd.extend(["--__NEBULA_CMD_5_bloh__", "__NEBULA_CMD_DUMMY_VALUE__"])
cmd.extend(["--__NEBULA_CMD_6_--output-prefix__", "__NEBULA_CMD_DUMMY_VALUE__"])
cmd.extend(["--__NEBULA_CMD_7_s3://fake-bucket__", "__NEBULA_CMD_DUMMY_VALUE__"])
cmd.extend(["--__NEBULA_CMD_8_--inputs__", "__NEBULA_CMD_DUMMY_VALUE__"])
cmd.extend(["--__NEBULA_CMD_9_s3://fake-bucket__", "__NEBULA_CMD_DUMMY_VALUE__"])


@mock.patch.dict("os.environ")
@mock.patch("subprocess.run")
def test(mock_subprocess_run):
    _nebula_sagemaker_run(cmd)
    assert "env1" in os.environ
    assert "env2" in os.environ
    assert os.environ["env1"] == "val1"
    assert os.environ["env2"] == "val2"
    mock_subprocess_run.assert_called_with(
        "service_venv pynebula-execute --task-module blah --task-name bloh "
        "--output-prefix s3://fake-bucket --inputs s3://fake-bucket".split(),
        stdout=sys.stdout,
        stderr=sys.stderr,
        encoding="utf-8",
        check=True,
    )
