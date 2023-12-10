"""
======================================
:mod:`nebulakit.core.local_fsspec`
======================================

.. currentmodule:: nebulakit.core.local_fsspec


.. autosummary::
   :toctree: generated/
   :template: custom.rst
   :nosignatures:

   NebulaLocalFileSystem

"""
import os

from fsspec.implementations.local import LocalFileSystem


class NebulaLocalFileSystem(LocalFileSystem):  # noqa
    """
    This class doesn't do anything except override the separator so that it works on windows
    """

    sep = os.sep
