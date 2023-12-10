from click.testing import CliRunner

from nebulakit.clis.sdk_in_container import pynebula


def test_pynebula_serve():
    runner = CliRunner()
    result = runner.invoke(pynebula.main, ["serve", "agent", "--port", "0", "--timeout", "1"], catch_exceptions=False)
    assert result.exit_code == 0
