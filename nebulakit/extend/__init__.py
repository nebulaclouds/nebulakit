"""
==================
Extending Nebulakit
==================

.. currentmodule:: nebulakit.extend

This package contains things that are useful when extending Nebulakit.

.. autosummary::
   :toctree: generated/

   get_serializable
   context_manager
   IgnoreOutputs
   ExecutionState
   Image
   ImageConfig
   Interface
   Promise
   TaskPlugins
   DictTransformer
   T
   TypeEngine
   TypeTransformer
   PythonCustomizedContainerTask
   ExecutableTemplateShimTask
   ShimTaskExecutor
"""

from nebulakit.configuration import Image, ImageConfig, SerializationSettings
from nebulakit.core import context_manager
from nebulakit.core.base_sql_task import SQLTask
from nebulakit.core.base_task import IgnoreOutputs, PythonTask, TaskResolverMixin
from nebulakit.core.class_based_resolver import ClassStorageTaskResolver
from nebulakit.core.context_manager import ExecutionState, SecretsManager
from nebulakit.core.data_persistence import FileAccessProvider
from nebulakit.core.interface import Interface
from nebulakit.core.promise import Promise
from nebulakit.core.python_customized_container_task import PythonCustomizedContainerTask
from nebulakit.core.shim_task import ExecutableTemplateShimTask, ShimTaskExecutor
from nebulakit.core.task import TaskPlugins
from nebulakit.core.type_engine import DictTransformer, T, TypeEngine, TypeTransformer
from nebulakit.tools.translator import get_serializable
