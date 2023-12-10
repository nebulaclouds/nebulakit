"""
=====================
Unit Testing
=====================

.. currentmodule:: nebulakit.testing

The imports exposed in this package will help you unit test your Nebula tasks. These are particularly helpful when
testing workflows that contain tasks that cannot run locally (a Hive task for instance).

.. autosummary::
   :toctree: generated/

   patch - A decorator similar to the regular one you're probably used to
   task_mock - Non-decorative function

"""

from nebulakit.core.context_manager import SecretsManager
from nebulakit.core.testing import patch, task_mock
