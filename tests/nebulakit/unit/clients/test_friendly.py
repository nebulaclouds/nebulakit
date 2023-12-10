from datetime import timedelta

import mock as _mock
from nebulaidl.admin import project_pb2 as _project_pb2
from nebulaidl.service import dataproxy_pb2 as _data_proxy_pb2
from google.protobuf.duration_pb2 import Duration

from nebulakit.clients.friendly import SynchronousNebulaClient as _SynchronousNebulaClient
from nebulakit.configuration import PlatformConfig
from nebulakit.models.project import Project as _Project


@_mock.patch("nebulakit.clients.friendly._RawSynchronousNebulaClient.update_project")
def test_update_project(mock_raw_update_project):
    client = _SynchronousNebulaClient(PlatformConfig.for_endpoint("a.b.com", True))
    project = _Project("foo", "name", "description", state=_Project.ProjectState.ACTIVE)
    client.update_project(project)
    mock_raw_update_project.assert_called_with(project.to_nebula_idl())


@_mock.patch("nebulakit.clients.friendly._RawSynchronousNebulaClient.list_projects")
def test_list_projects_paginated(mock_raw_list_projects):
    client = _SynchronousNebulaClient(PlatformConfig.for_endpoint("a.b.com", True))
    client.list_projects_paginated(limit=100, token="")
    project_list_request = _project_pb2.ProjectListRequest(limit=100, token="", filters=None, sort_by=None)
    mock_raw_list_projects.assert_called_with(project_list_request=project_list_request)


@_mock.patch("nebulakit.clients.friendly._RawSynchronousNebulaClient.create_upload_location")
def test_create_upload_location(mock_raw_create_upload_location):
    client = _SynchronousNebulaClient(PlatformConfig.for_endpoint("a.b.com", True))
    client.get_upload_signed_url("foo", "bar", bytes(), "baz.qux", timedelta(minutes=42))
    duration_pb = Duration()
    duration_pb.FromTimedelta(timedelta(minutes=42))
    create_upload_location_request = _data_proxy_pb2.CreateUploadLocationRequest(
        project="foo", domain="bar", filename="baz.qux", expires_in=duration_pb
    )
    mock_raw_create_upload_location.assert_called_with(create_upload_location_request)
