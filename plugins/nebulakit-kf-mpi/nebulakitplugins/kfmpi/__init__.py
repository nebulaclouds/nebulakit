"""
.. currentmodule:: nebulakitplugins.kfmpi

This package contains things that are useful when extending Nebulakit.

.. autosummary::
   :template: custom.rst
   :toctree: generated/

   MPIJob
"""

from .task import CleanPodPolicy, HorovodJob, Launcher, MPIJob, RestartPolicy, RunPolicy, Worker
