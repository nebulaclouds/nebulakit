from datetime import datetime, timedelta

import click
import pytest
from click.testing import CliRunner
from mock import mock

from nebulakit.clis.sdk_in_container import pynebula
from nebulakit.clis.sdk_in_container.backfill import resolve_backfill_window
from nebulakit.remote import NebulaRemote


def test_resolve_backfill_window():
    dt = datetime(2022, 12, 1, 8)
    window = timedelta(days=10)
    assert resolve_backfill_window(None, dt + window, window) == (dt, dt + window)
    assert resolve_backfill_window(dt, None, window) == (dt, dt + window)
    assert resolve_backfill_window(dt, dt + window) == (dt, dt + window)
    with pytest.raises(click.BadParameter):
        resolve_backfill_window()


@mock.patch("nebulakit.clis.sdk_in_container.helpers.NebulaRemote", spec=NebulaRemote)
def test_pynebula_backfill(mock_remote):
    mock_remote.generate_console_url.return_value = "ex"
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            pynebula.main,
            [
                "backfill",
                "--parallel",
                "-p",
                "nebulasnacks",
                "-d",
                "development",
                "--from-date",
                "now",
                "--backfill-window",
                "5 day",
                "daily",
            ],
        )
        assert result.exit_code == 0
        assert "Execution launched" in result.output
