from unittest import mock

from nebulaidl.admin import project_pb2 as _project_pb2

from nebulakit.clients.raw import RawSynchronousNebulaClient
from nebulakit.configuration import PlatformConfig


@mock.patch("nebulakit.clients.raw._admin_service")
@mock.patch("nebulakit.clients.raw.grpc.insecure_channel")
def test_update_project(mock_channel, mock_admin):
    client = RawSynchronousNebulaClient(PlatformConfig(endpoint="a.b.com", insecure=True))
    project = _project_pb2.Project(id="foo", name="name", description="description", state=_project_pb2.Project.ACTIVE)
    client.update_project(project)
    mock_admin.AdminServiceStub().UpdateProject.assert_called_with(project, metadata=None)


@mock.patch("nebulakit.clients.raw._admin_service")
@mock.patch("nebulakit.clients.raw.grpc.insecure_channel")
def test_list_projects_paginated(mock_channel, mock_admin):
    client = RawSynchronousNebulaClient(PlatformConfig(endpoint="a.b.com", insecure=True))
    project_list_request = _project_pb2.ProjectListRequest(limit=100, token="", filters=None, sort_by=None)
    client.list_projects(project_list_request)
    mock_admin.AdminServiceStub().ListProjects.assert_called_with(project_list_request, metadata=None)
