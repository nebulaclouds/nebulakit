"""
Nebulakit Directory Type
==========================================================
.. currentmodule:: nebulakit.types.directory

Similar to :py:class:`nebulakit.types.file.NebulaFile` there are some 'preformatted' directory types.

.. autosummary::
   :toctree: generated/
   :template: file_types.rst

   NebulaDirectory
   TensorboardLogs
   TFRecordsDirectory
"""

import typing

from .types import NebulaDirectory

# The following section provides some predefined aliases for commonly used NebulaDirectory formats.

tensorboard = typing.TypeVar("tensorboard")
TensorboardLogs = NebulaDirectory[tensorboard]
"""
    This type can be used to denote that the output is a folder that contains logs that can be loaded in TensorBoard.
    This is usually the SummaryWriter output in PyTorch or Keras callbacks which record the history readable by
    TensorBoard.
"""

tfrecords_dir = typing.TypeVar("tfrecords_dir")
TFRecordsDirectory = NebulaDirectory[tfrecords_dir]
"""
    This type can be used to denote that the output is a folder that contains tensorflow record files.
    This is usually the TFRecordWriter output in Tensorflow which writes serialised tf.train.Example
    message (or protobuf) to tfrecord files
"""
