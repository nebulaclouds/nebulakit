import pickle
from datetime import timedelta
from unittest import mock
from unittest.mock import MagicMock

import grpc
import pytest
from aioresponses import aioresponses
from nebulaidl.admin.agent_pb2 import SUCCEEDED
from nebulakitplugins.spark.agent import Metadata, get_header, DATABRICKS_API_ENDPOINT

from nebulakit.extend.backend.base_agent import AgentRegistry
from nebulakit.interfaces.cli_identifiers import Identifier
from nebulakit.models import literals, task
from nebulakit.models.core.identifier import ResourceType
from nebulakit.models.task import Container, Resources, TaskTemplate


@pytest.mark.asyncio
async def test_databricks_agent():
    ctx = MagicMock(spec=grpc.ServicerContext)
    agent = AgentRegistry.get_agent("spark")

    task_id = Identifier(
        resource_type=ResourceType.TASK, project="project", domain="domain", name="name", version="version"
    )
    task_metadata = task.TaskMetadata(
        True,
        task.RuntimeMetadata(task.RuntimeMetadata.RuntimeType.NEBULA_SDK, "1.0.0", "python"),
        timedelta(days=1),
        literals.RetryStrategy(3),
        True,
        "0.1.1b0",
        "This is deprecated!",
        True,
        "A",
    )
    task_config = {
        "sparkConf": {
            "spark.driver.memory": "1000M",
            "spark.executor.memory": "1000M",
            "spark.executor.cores": "1",
            "spark.executor.instances": "2",
            "spark.driver.cores": "1",
        },
        "mainApplicationFile": "dbfs:/entrypoint.py",
        "databricksConf": {
            "run_name": "nebulakit databricks plugin example",
            "new_cluster": {
                "spark_version": "12.2.x-scala2.12",
                "node_type_id": "n2-highmem-4",
                "num_workers": 1,
            },
            "timeout_seconds": 3600,
            "max_retries": 1,
        },
        "databricksInstance": "test-account.cloud.databricks.com",
    }
    container = Container(
        image="nebulaclouds/nebulakit:databricks-0.18.0-py3.7",
        command=[],
        args=[
            "pynebula-fast-execute",
            "--additional-distribution",
            "s3://my-s3-bucket/nebulasnacks/development/24UYJEF2HDZQN3SG4VAZSM4PLI======/script_mode.tar.gz",
            "--dest-dir",
            "/root",
            "--",
            "pynebula-execute",
            "--inputs",
            "s3://my-s3-bucket",
            "--output-prefix",
            "s3://my-s3-bucket",
            "--raw-output-data-prefix",
            "s3://my-s3-bucket",
            "--checkpoint-path",
            "s3://my-s3-bucket",
            "--prev-checkpoint",
            "s3://my-s3-bucket",
            "--resolver",
            "nebulakit.core.python_auto_container.default_task_resolver",
            "--",
            "task-module",
            "spark_local_example",
            "task-name",
            "hello_spark",
        ],
        resources=Resources(
            requests=[],
            limits=[],
        ),
        env={},
        config={},
    )

    dummy_template = TaskTemplate(
        id=task_id,
        custom=task_config,
        metadata=task_metadata,
        container=container,
        interface=None,
        type="spark",
    )
    mocked_token = "mocked_databricks_token"
    mocked_context = mock.patch("nebulakit.current_context", autospec=True).start()
    mocked_context.return_value.secrets.get.return_value = mocked_token

    metadata_bytes = pickle.dumps(
        Metadata(
            databricks_instance="test-account.cloud.databricks.com",
            run_id="123",
        )
    )

    mock_create_response = {"run_id": "123"}
    mock_get_response = {"run_id": "123", "state": {"result_state": "SUCCESS", "state_message": "OK"}}
    mock_delete_response = {}
    create_url = f"https://test-account.cloud.databricks.com{DATABRICKS_API_ENDPOINT}/runs/submit"
    get_url = f"https://test-account.cloud.databricks.com{DATABRICKS_API_ENDPOINT}/runs/get?run_id=123"
    delete_url = f"https://test-account.cloud.databricks.com{DATABRICKS_API_ENDPOINT}/runs/cancel"
    with aioresponses() as mocked:
        mocked.post(create_url, status=200, payload=mock_create_response)
        res = await agent.async_create(ctx, "/tmp", dummy_template, None)
        assert res.resource_meta == metadata_bytes

        mocked.get(get_url, status=200, payload=mock_get_response)
        res = await agent.async_get(ctx, metadata_bytes)
        assert res.resource.state == SUCCEEDED
        assert res.resource.outputs == literals.LiteralMap({}).to_nebula_idl()
        assert res.resource.message == "OK"

        mocked.post(delete_url, status=200, payload=mock_delete_response)
        await agent.async_delete(ctx, metadata_bytes)

    assert get_header() == {"Authorization": f"Bearer {mocked_token}", "content-type": "application/json"}

    mock.patch.stopall()
