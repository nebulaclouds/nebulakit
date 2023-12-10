import pytest
import tensorflow
import tensorflow as tf
from tensorflow.core.example.example_pb2 import Example
from tensorflow.python.data.ops.readers import TFRecordDatasetV2
from typing_extensions import Annotated

import nebulakit
from nebulakit.configuration import Image, ImageConfig
from nebulakit.core import context_manager
from nebulakit.extras.tensorflow.record import (
    TensorFlowRecordFileTransformer,
    TensorFlowRecordsDirTransformer,
    TFRecordDatasetConfig,
)
from nebulakit.models.core.types import BlobType
from nebulakit.models.literals import BlobMetadata
from nebulakit.models.types import LiteralType
from nebulakit.types.directory import TFRecordsDirectory
from nebulakit.types.file import TFRecordFile

from .test_record import features1, features2

default_img = Image(name="default", fqn="test", tag="tag")
serialization_settings = nebulakit.configuration.SerializationSettings(
    project="project",
    domain="domain",
    version="version",
    env=None,
    image_config=ImageConfig(default_image=default_img, images=[default_img]),
)


@pytest.mark.parametrize(
    "transformer,python_type,format,dimensionality",
    [
        (TensorFlowRecordFileTransformer(), TFRecordFile, TensorFlowRecordFileTransformer.TENSORFLOW_FORMAT, 0),
        (TensorFlowRecordsDirTransformer(), TFRecordsDirectory, TensorFlowRecordsDirTransformer.TENSORFLOW_FORMAT, 1),
    ],
)
def test_get_literal_type(transformer, python_type, format, dimensionality):
    tf = transformer
    lt = tf.get_literal_type(python_type)
    assert lt == LiteralType(blob=BlobType(format=format, dimensionality=dimensionality))


@pytest.mark.parametrize(
    "transformer,python_type,format,python_val,dimension",
    [
        (
            TensorFlowRecordFileTransformer(),
            TFRecordFile,
            TensorFlowRecordFileTransformer.TENSORFLOW_FORMAT,
            tf.train.Example(features=features1),
            BlobType.BlobDimensionality.SINGLE,
        ),
        (
            TensorFlowRecordsDirTransformer(),
            TFRecordsDirectory,
            TensorFlowRecordsDirTransformer.TENSORFLOW_FORMAT,
            [tf.train.Example(features=features1), tf.train.Example(features=features2)],
            BlobType.BlobDimensionality.MULTIPART,
        ),
    ],
)
def test_to_python_value_and_literal(transformer, python_type, format, python_val, dimension):
    ctx = context_manager.NebulaContext.current_context()
    tf = transformer
    lt = tf.get_literal_type(python_type)
    lv = tf.to_literal(ctx, python_val, type(python_val), lt)  # type: ignore
    assert lv.scalar.blob.metadata == BlobMetadata(
        type=BlobType(
            format=format,
            dimensionality=dimension,
        )
    )
    assert lv.scalar.blob.uri is not None
    output = tf.to_python_value(ctx, lv, Annotated[python_type, TFRecordDatasetConfig(buffer_size=1024)])
    assert isinstance(output, TFRecordDatasetV2)
    results = []
    example = tensorflow.train.Example()
    for raw_record in output:
        example.ParseFromString(raw_record.numpy())
        results.append(example)
    if isinstance(python_val, list):
        assert len(results) == 2
        assert all(list(map(lambda x: isinstance(x, Example), python_val)))
    else:
        assert results == [python_val]
