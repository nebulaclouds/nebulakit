import pytest
from click.testing import CliRunner
from mock import mock

from nebulakit.clis.sdk_in_container import pynebula
from nebulakit.remote import NebulaRemote


@mock.patch("nebulakit.clis.sdk_in_container.helpers.NebulaRemote", spec=NebulaRemote)
@pytest.mark.parametrize(
    ("action", "expected_state"),
    [
        ("activate", "ACTIVE"),
        ("deactivate", "INACTIVE"),
    ],
)
def test_pynebula_launchplan(mock_remote, action, expected_state):
    mock_remote.generate_console_url.return_value = "ex"
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            pynebula.main,
            [
                "launchplan",
                f"--{action}",
                "-p",
                "nebulasnacks",
                "-d",
                "development",
                "daily",
            ],
        )
        assert result.exit_code == 0
        assert f"Launchplan was set to {expected_state}: " in result.output
