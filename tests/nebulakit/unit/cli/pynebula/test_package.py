import os
import shutil

from click.testing import CliRunner

import nebulakit
import nebulakit.clis.sdk_in_container.utils
import nebulakit.configuration
import nebulakit.tools.serialize_helpers
from nebulakit import TaskMetadata
from nebulakit.clis.sdk_in_container import pynebula
from nebulakit.core import context_manager
from nebulakit.models.admin.workflow import WorkflowSpec
from nebulakit.models.core.identifier import Identifier, ResourceType
from nebulakit.models.launch_plan import LaunchPlan
from nebulakit.models.task import TaskSpec
from nebulakit.remote import NebulaTask
from nebulakit.remote.interface import TypedInterface
from nebulakit.remote.remote_callable import RemoteEntity

sample_file_contents = """
from nebulakit import task, workflow

@task(cache=True, cache_version="1", retries=3)
def sum(x: int, y: int) -> int:
    return x + y

@task(cache=True, cache_version="1", retries=3)
def square(z: int) -> int:
    return z*z

@workflow
def my_workflow(x: int, y: int) -> int:
    return sum(x=square(z=x), y=square(z=y))
"""


@nebulakit.task
def foo():
    pass


@nebulakit.workflow
def wf():
    return foo()


def test_get_registrable_entities():
    ctx = context_manager.NebulaContextManager.current_context().with_serialization_settings(
        nebulakit.configuration.SerializationSettings(
            project="p",
            domain="d",
            version="v",
            image_config=nebulakit.configuration.ImageConfig(
                default_image=nebulakit.configuration.Image("def", "docker.io/def", "latest")
            ),
        )
    )
    context_manager.NebulaEntities.entities = [
        foo,
        wf,
        "str",
        NebulaTask(
            id=Identifier(ResourceType.TASK, "p", "d", "n", "v"),
            type="t",
            metadata=TaskMetadata().to_taskmetadata_model(),
            interface=TypedInterface(inputs={}, outputs={}),
            custom=None,
        ),
    ]
    entities = nebulakit.tools.serialize_helpers.get_registrable_entities(ctx)
    assert entities
    assert len(entities) == 3

    for e in entities:
        if isinstance(e, RemoteEntity):
            assert False, "found unexpected remote entity"
        if isinstance(e, WorkflowSpec) or isinstance(e, TaskSpec) or isinstance(e, LaunchPlan):
            continue
        assert False, f"found unknown entity {type(e)}"


def test_package_with_fast_registration():
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.makedirs("core", exist_ok=True)
        with open(os.path.join("core", "sample.py"), "w") as f:
            f.write(sample_file_contents)
            f.close()
        result = runner.invoke(pynebula.main, ["--pkgs", "core", "package", "--image", "core:v1", "--fast"])
        assert result.exit_code == 0
        assert "Successfully serialized" in result.output
        assert "Successfully packaged" in result.output
        result = runner.invoke(pynebula.main, ["--pkgs", "core", "package", "--image", "core:v1", "--fast"])
        assert result.exit_code == 2
        assert "nebula-package.tgz already exists, specify -f to override" in result.output
        result = runner.invoke(
            pynebula.main,
            ["--pkgs", "core", "package", "--image", "core:v1", "--fast", "--force"],
        )
        assert result.exit_code == 0
        assert "deleting and re-creating it" in result.output
        shutil.rmtree("core")


def test_package():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            pynebula.main,
            [
                "--pkgs",
                "nebulakit.unit.cli.pynebula.test_package",
                "package",
                "--image",
                "myapp:03eccc1cf101adbd8c4734dba865d3fdeb720aa7",
            ],
        )
        assert result.exit_code == 1
        assert result.output is not None


def test_pkgs():
    pp = nebulakit.clis.sdk_in_container.utils.validate_package(None, None, ["a.b", "a.c,b.a", "cc.a"])
    assert pp == ["a.b", "a.c", "b.a", "cc.a"]


def test_package_with_no_pkgs():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(pynebula.main, ["package"])
        assert result.exit_code == 1
        assert "No packages to scan for nebula entities. Aborting!" in result.output
