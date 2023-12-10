import tempfile

import pytest
from click.testing import CliRunner

from nebulakit.clis.sdk_in_container import pynebula


@pytest.mark.parametrize(
    "command",
    [
        ["example"],
        ["example", "--template", "simple-example"],
        ["example", "--template", "bayesian-optimization"],
    ],
)
def test_pynebula_init(command, monkeypatch: pytest.MonkeyPatch):
    tmp_dir = tempfile.mkdtemp()
    monkeypatch.chdir(tmp_dir)
    runner = CliRunner()
    result = runner.invoke(
        pynebula.init,
        command,
        catch_exceptions=True,
    )
    assert result.exit_code == 0
