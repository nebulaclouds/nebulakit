"""
.. currentmodule:: nebulakitplugins.kfpytorch

This package contains things that are useful when extending Nebulakit.

.. autosummary::
   :template: custom.rst
   :toctree: generated/

   PyTorch
   Elastic
"""

from .task import CleanPodPolicy, Elastic, Master, PyTorch, RestartPolicy, RunPolicy, Worker
