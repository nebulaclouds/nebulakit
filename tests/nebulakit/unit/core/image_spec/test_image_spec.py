import os

import pytest

from nebulakit.core import context_manager
from nebulakit.core.context_manager import ExecutionState
from nebulakit.image_spec import ImageSpec
from nebulakit.image_spec.image_spec import _F_IMG_ID, ImageBuildEngine, calculate_hash_from_image_spec

REQUIREMENT_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
REGISTRY_CONFIG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "registry_config.json")


def test_image_spec(mock_image_spec_builder):
    image_spec = ImageSpec(
        name="NEBULAKIT",
        builder="dummy",
        packages=["pandas"],
        apt_packages=["git"],
        python_version="3.8",
        registry="",
        base_image="cr.nebula.org/nebulaclouds/nebulakit:py3.8-latest",
        cuda="11.2.2",
        cudnn="8",
        requirements=REQUIREMENT_FILE,
        registry_config=REGISTRY_CONFIG_FILE,
    )

    assert image_spec.python_version == "3.8"
    assert image_spec.base_image == "cr.nebula.org/nebulaclouds/nebulakit:py3.8-latest"
    assert image_spec.packages == ["pandas"]
    assert image_spec.apt_packages == ["git"]
    assert image_spec.registry == ""
    assert image_spec.requirements == REQUIREMENT_FILE
    assert image_spec.registry_config == REGISTRY_CONFIG_FILE
    assert image_spec.cuda == "11.2.2"
    assert image_spec.cudnn == "8"
    assert image_spec.name == "nebulakit"
    assert image_spec.builder == "dummy"
    assert image_spec.source_root is None
    assert image_spec.env is None
    assert image_spec.pip_index is None
    assert image_spec.is_container() is True

    tag = calculate_hash_from_image_spec(image_spec)
    assert image_spec.image_name() == f"nebulakit:{tag}"
    ctx = context_manager.NebulaContext.current_context()
    with context_manager.NebulaContextManager.with_context(
        ctx.with_execution_state(ctx.execution_state.with_params(mode=ExecutionState.Mode.TASK_EXECUTION))
    ):
        os.environ[_F_IMG_ID] = "nebulakit:123"
        assert image_spec.is_container() is False

    ImageBuildEngine.register("dummy", mock_image_spec_builder)
    ImageBuildEngine.build(image_spec)

    assert "dummy" in ImageBuildEngine._REGISTRY
    assert calculate_hash_from_image_spec(image_spec) == tag
    assert image_spec.exist() is False

    # Remove the dummy builder, and build the image again
    # The image has already been built, so it shouldn't fail.
    del ImageBuildEngine._REGISTRY["dummy"]
    ImageBuildEngine.build(image_spec)

    with pytest.raises(Exception):
        image_spec.builder = "nebula"
        ImageBuildEngine.build(image_spec)
