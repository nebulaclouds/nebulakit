import os
import sys

import mock
import pytest

from nebulakit.configuration import ImageConfig
from nebulakit.configuration.default_images import DefaultImages, PythonVersion


@pytest.mark.parametrize(
    "python_version_enum, expected_image_string",
    [
        (PythonVersion.PYTHON_3_8, "cr.nebula.org/nebulaclouds/nebulakit:py3.8-latest"),
        (PythonVersion.PYTHON_3_9, "cr.nebula.org/nebulaclouds/nebulakit:py3.9-latest"),
        (PythonVersion.PYTHON_3_10, "cr.nebula.org/nebulaclouds/nebulakit:py3.10-latest"),
    ],
)
def test_defaults(python_version_enum, expected_image_string):
    assert DefaultImages.find_image_for(python_version_enum) == expected_image_string


@pytest.mark.parametrize(
    "python_version_enum, nebulakit_version, expected_image_string",
    [
        (PythonVersion.PYTHON_3_9, "v0.32.0", "cr.nebula.org/nebulaclouds/nebulakit:py3.9-0.32.0"),
        (PythonVersion.PYTHON_3_8, "1.31.3", "cr.nebula.org/nebulaclouds/nebulakit:py3.8-1.31.3"),
    ],
)
def test_set_both(python_version_enum, nebulakit_version, expected_image_string):
    assert DefaultImages.find_image_for(python_version_enum, nebulakit_version) == expected_image_string


def test_image_config_auto():
    x = ImageConfig.auto_default_image()
    assert x.images[0].name == "default"
    version_str = f"{sys.version_info.major}.{sys.version_info.minor}"
    assert x.images[0].full == f"cr.nebula.org/nebulaclouds/nebulakit:py{version_str}-latest"


def test_image_from_nebulactl_config():
    os.environ["NEBULACTL_CONFIG"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "configs/sample.yaml")
    image_config = ImageConfig.auto(config_file=None)
    assert image_config.images[0].full == "docker.io/xyz:latest"
    assert image_config.images[1].full == "docker.io/abc:None"


@mock.patch("nebulakit.configuration.default_images.sys")
def test_not_version(mock_sys):
    mock_sys.version_info.major.return_value = 2
    # Python version 2 not in enum
    with pytest.raises(ValueError):
        DefaultImages.default_image()


def test_image_create():
    with pytest.raises(ValueError):
        ImageConfig.create_from("cr.nebula.org/im/g:latest")

    ic = ImageConfig.from_images("cr.nebula.org/im/g:latest")
    assert ic.default_image.fqn == "cr.nebula.org/im/g"


def test_get_version_suffix():
    assert DefaultImages.get_version_suffix() == "latest"
