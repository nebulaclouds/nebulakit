"""
.. currentmodule:: nebulakitplugins.papermill

This package contains things that are useful when extending Nebulakit.

.. autosummary::
   :template: custom.rst
   :toctree: generated/

   NotebookTask
   record_outputs
"""

from .task import NotebookTask, load_nebuladirectory, load_nebulafile, load_structureddataset, record_outputs
