from collections import OrderedDict

import pytest
from nebulakitplugins.athena import AthenaConfig, AthenaTask

from nebulakit import kwtypes, workflow
from nebulakit.configuration import Image, ImageConfig, SerializationSettings
from nebulakit.extend import get_serializable
from nebulakit.types.schema import NebulaSchema


def test_serialization():
    athena_task = AthenaTask(
        name="nebulakit.demo.athena_task.query",
        inputs=kwtypes(ds=str),
        task_config=AthenaConfig(database="mnist", catalog="my_catalog", workgroup="my_wg"),
        query_template="""
            insert overwrite directory '{{ .rawOutputDataPrefix }}' stored as parquet
            select *
            from blah
            where ds = '{{ .Inputs.ds }}'
        """,
        # the schema literal's backend uri will be equal to the value of .raw_output_data
        output_schema_type=NebulaSchema,
    )

    @workflow
    def my_wf(ds: str) -> NebulaSchema:
        return athena_task(ds=ds)

    default_img = Image(name="default", fqn="test", tag="tag")
    serialization_settings = SerializationSettings(
        project="proj",
        domain="dom",
        version="123",
        image_config=ImageConfig(default_image=default_img, images=[default_img]),
        env={},
    )
    task_spec = get_serializable(OrderedDict(), serialization_settings, athena_task)
    assert "{{ .rawOutputDataPrefix" in task_spec.template.custom["statement"]
    assert "insert overwrite directory" in task_spec.template.custom["statement"]
    assert "mnist" == task_spec.template.custom["schema"]
    assert "my_catalog" == task_spec.template.custom["catalog"]
    assert "my_wg" == task_spec.template.custom["routingGroup"]
    assert len(task_spec.template.interface.inputs) == 1
    assert len(task_spec.template.interface.outputs) == 1

    admin_workflow_spec = get_serializable(OrderedDict(), serialization_settings, my_wf)
    assert admin_workflow_spec.template.interface.outputs["o0"].type.schema is not None
    assert admin_workflow_spec.template.outputs[0].var == "o0"
    assert admin_workflow_spec.template.outputs[0].binding.promise.node_id == "n0"
    assert admin_workflow_spec.template.outputs[0].binding.promise.var == "results"


def test_local_exec():
    athena_task = AthenaTask(
        name="nebulakit.demo.athena_task.query2",
        inputs=kwtypes(ds=str),
        query_template="""
            insert overwrite directory '{{ .rawOutputDataPrefix }}' stored as parquet
            select *
            from blah
            where ds = '{{ .Inputs.ds }}'
        """,
        # the schema literal's backend uri will be equal to the value of .raw_output_data
        output_schema_type=NebulaSchema,
    )

    assert len(athena_task.interface.inputs) == 1
    assert len(athena_task.interface.outputs) == 1

    # will not run locally
    with pytest.raises(Exception):
        athena_task()
