import mock as _mock
import pytest
from click.testing import CliRunner as _CliRunner

from nebulakit.clis.nebula_cli import main as _main
from nebulakit.exceptions.user import NebulaAssertion
from nebulakit.models import filters as _filters
from nebulakit.models.admin import common as _admin_common
from nebulakit.models.core import identifier as _core_identifier
from nebulakit.models.project import Project as _Project

mm = _mock.MagicMock()
mm.return_value = 100


@_mock.patch("nebulakit.clis.nebula_cli.main.utils")
def test__extract_files_with_unspecified_resource_type(load_mock):
    id = _core_identifier.Identifier(
        _core_identifier.ResourceType.UNSPECIFIED,
        "myproject",
        "development",
        "name",
        "v",
    )

    load_mock.load_proto_from_file.return_value = id.to_nebula_idl()
    with pytest.raises(NebulaAssertion):
        _main._extract_pair("a", "b", "mynebulaproject", "development", "v", {})


def _identity_dummy(a, b, project, domain, version, patches):
    return (a, b)


@_mock.patch("nebulakit.clis.nebula_cli.main._extract_pair", new=_identity_dummy)
def test__extract_files_pair_iterator():
    results = _main._extract_files("mynebulaproject", "development", "v", ["1.pb", "2.pb"], None)
    assert [("1.pb", 1), ("2.pb", 2)] == results


@_mock.patch("nebulakit.clis.nebula_cli.main._friendly_client.SynchronousNebulaClient")
def test_list_projects(mock_client):
    mock_client().list_projects_paginated.return_value = ([], "")
    runner = _CliRunner()
    result = runner.invoke(
        _main._nebula_cli, ["list-projects", "-h", "a.b.com", "-i", "--filter", "ne(state,-1)", "--sort-by", "asc(name)"]
    )
    assert result.exit_code == 0
    mock_client().list_projects_paginated.assert_called_with(
        limit=100,
        token="",
        filters=[_filters.Filter.from_python_std("ne(state,-1)")],
        sort_by=_admin_common.Sort.from_python_std("asc(name)"),
    )


@_mock.patch("nebulakit.clis.nebula_cli.main._friendly_client.SynchronousNebulaClient")
def test_archive_project(mock_client):
    runner = _CliRunner()
    result = runner.invoke(_main._nebula_cli, ["archive-project", "-p", "foo", "-h", "a.b.com", "-i"])
    assert result.exit_code == 0
    mock_client().update_project.assert_called_with(_Project.archived_project("foo"))


@_mock.patch("nebulakit.clis.nebula_cli.main._friendly_client.SynchronousNebulaClient")
def test_activate_project(mock_client):
    runner = _CliRunner()
    result = runner.invoke(_main._nebula_cli, ["activate-project", "-p", "foo", "-h", "a.b.com", "-i"])
    assert result.exit_code == 0
    mock_client().update_project.assert_called_with(_Project.active_project("foo"))
