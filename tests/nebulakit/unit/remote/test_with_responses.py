import os
import typing
from collections import OrderedDict

import mock
from nebulaidl.admin import launch_plan_pb2, task_pb2, workflow_pb2

import nebulakit.configuration
from nebulakit.configuration import Config, ImageConfig
from nebulakit.configuration.default_images import DefaultImages
from nebulakit.core.node_creation import create_node
from nebulakit.core.utils import load_proto_from_file
from nebulakit.core.workflow import workflow
from nebulakit.models import launch_plan as launch_plan_models
from nebulakit.models import task as task_models
from nebulakit.models.admin import workflow as admin_workflow_models
from nebulakit.remote.remote import NebulaRemote
from nebulakit.tools.translator import get_serializable

rr = NebulaRemote(
    Config.for_sandbox(),
    default_project="nebulasnacks",
    default_domain="development",
)

responses_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "responses")


@mock.patch("nebulakit.remote.remote.NebulaRemote.client")
def test_fetch_wf_wf_lp_pattern(mock_client):
    leaf_lp = load_proto_from_file(
        launch_plan_pb2.LaunchPlan,
        os.path.join(responses_dir, "admin.launch_plan_pb2.LaunchPlan_core.control_flow.subworkflows.leaf_subwf.pb"),
    )
    leaf_lp = launch_plan_models.LaunchPlan.from_nebula_idl(leaf_lp)
    root_wf = load_proto_from_file(
        workflow_pb2.Workflow,
        os.path.join(responses_dir, "admin.workflow_pb2.Workflow_core.control_flow.subworkflows.root_level_wf.pb"),
    )
    root_wf = admin_workflow_models.Workflow.from_nebula_idl(root_wf)

    mock_client.get_workflow.return_value = root_wf
    mock_client.get_launch_plan.return_value = leaf_lp
    fwf = rr.fetch_workflow(name="core.control_flow.subworkflows.root_level_wf", version="JiepXcXB3SiEJ8pwYDy-7g==")
    assert len(fwf.sub_workflows) == 2


@mock.patch("nebulakit.remote.remote.NebulaRemote.client")
def test_task(mock_client):
    merge_sort_remotely = load_proto_from_file(
        task_pb2.Task,
        os.path.join(responses_dir, "admin.task_pb2.Task.pb"),
    )
    admin_task = task_models.Task.from_nebula_idl(merge_sort_remotely)
    mock_client.get_task.return_value = admin_task
    ft = rr.fetch_task(name="merge_sort_remotely", version="tst")
    assert len(ft.interface.inputs) == 2
    assert len(ft.interface.outputs) == 1


@mock.patch("nebulakit.remote.remote.NebulaRemote.client")
def test_normal_task(mock_client):
    merge_sort_remotely = load_proto_from_file(
        task_pb2.Task,
        os.path.join(responses_dir, "admin.task_pb2.Task.pb"),
    )
    admin_task = task_models.Task.from_nebula_idl(merge_sort_remotely)
    mock_client.get_task.return_value = admin_task
    remote_task = rr.fetch_task(name="merge_sort_remotely", version="tst")

    @workflow
    def my_wf(numbers: typing.List[int], run_local_at_count: int) -> typing.List[int]:
        t1_node = create_node(remote_task, numbers=numbers, run_local_at_count=run_local_at_count)
        return t1_node.o0

    serialization_settings = nebulakit.configuration.SerializationSettings(
        project="project",
        domain="domain",
        version="version",
        env=None,
        image_config=ImageConfig.auto(img_name=DefaultImages.default_image()),
    )
    wf_spec = get_serializable(OrderedDict(), serialization_settings, my_wf)
    assert wf_spec.template.nodes[0].task_node.reference_id.name == "merge_sort_remotely"
