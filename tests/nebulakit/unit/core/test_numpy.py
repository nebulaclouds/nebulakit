from collections import OrderedDict

import numpy as np
from numpy.testing import assert_array_equal

import nebulakit
from nebulakit import task
from nebulakit.configuration import Image, ImageConfig
from nebulakit.core import context_manager
from nebulakit.models.core.types import BlobType
from nebulakit.models.literals import BlobMetadata
from nebulakit.models.types import LiteralType
from nebulakit.tools.translator import get_serializable
from nebulakit.types.numpy import NumpyArrayTransformer

default_img = Image(name="default", fqn="test", tag="tag")
serialization_settings = nebulakit.configuration.SerializationSettings(
    project="project",
    domain="domain",
    version="version",
    env=None,
    image_config=ImageConfig(default_image=default_img, images=[default_img]),
)


def test_get_literal_type():
    tf = NumpyArrayTransformer()
    lt = tf.get_literal_type(np.ndarray)
    assert lt == LiteralType(
        blob=BlobType(
            format=NumpyArrayTransformer.NUMPY_ARRAY_FORMAT, dimensionality=BlobType.BlobDimensionality.SINGLE
        )
    )


def test_to_python_value_and_literal():
    ctx = context_manager.NebulaContext.current_context()
    tf = NumpyArrayTransformer()
    python_val = np.array([1, 2, 3])
    lt = tf.get_literal_type(np.ndarray)

    lv = tf.to_literal(ctx, python_val, type(python_val), lt)  # type: ignore
    assert lv.scalar.blob.metadata == BlobMetadata(
        type=BlobType(
            format=NumpyArrayTransformer.NUMPY_ARRAY_FORMAT,
            dimensionality=BlobType.BlobDimensionality.SINGLE,
        )
    )
    assert lv.scalar.blob.uri is not None

    output = tf.to_python_value(ctx, lv, np.ndarray)
    assert_array_equal(output, python_val)


def test_example():
    @task
    def t1(array: np.ndarray) -> np.ndarray:
        return array.flatten()

    task_spec = get_serializable(OrderedDict(), serialization_settings, t1)
    assert task_spec.template.interface.outputs["o0"].type.blob.format is NumpyArrayTransformer.NUMPY_ARRAY_FORMAT
