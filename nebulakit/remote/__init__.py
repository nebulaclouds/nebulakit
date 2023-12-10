"""
=====================
Remote Access
=====================

.. currentmodule:: nebulakit.remote

This module provides utilities for performing operations on tasks, workflows, launchplans, and executions, for example,
the following code fetches and executes a workflow:

.. code-block:: python

    # create a remote object from nebula config and environment variables
    NebulaRemote(config=Config.auto())
    NebulaRemote(config=Config.auto(config_file=....))
    NebulaRemote(config=Config(....))

    # Or if you need to specify a custom cert chain
    # (options and compression are also respected keyword arguments)
    NebulaRemote(private_key=your_private_key_bytes, root_certificates=..., certificate_chain=...)

    # fetch a workflow from the nebula backend
    remote = NebulaRemote(...)
    nebula_workflow = remote.fetch_workflow(name="my_workflow", version="v1")

    # execute the workflow, wait=True will return the execution object after it's completed
    workflow_execution = remote.execute(nebula_workflow, inputs={"a": 1, "b": 10}, wait=True)

    # inspect the execution's outputs
    print(workflow_execution.outputs)

.. _remote-entrypoint:

Entrypoint
==========

.. autosummary::
   :template: custom.rst
   :toctree: generated/
   :nosignatures:

   ~remote.NebulaRemote
   ~remote.Options

.. _remote-nebula-entities:

Entities
========

.. autosummary::
   :template: custom.rst
   :toctree: generated/
   :nosignatures:

   ~entities.NebulaTask
   ~entities.NebulaWorkflow
   ~entities.NebulaLaunchPlan

.. _remote-nebula-entity-components:

Entity Components
=================

.. autosummary::
   :template: custom.rst
   :toctree: generated/
   :nosignatures:

   ~entities.NebulaNode
   ~entities.NebulaTaskNode
   ~entities.NebulaWorkflowNode

.. _remote-nebula-execution-objects:

Execution Objects
=================

.. autosummary::
   :template: custom.rst
   :toctree: generated/
   :nosignatures:

   ~executions.NebulaWorkflowExecution
   ~executions.NebulaTaskExecution
   ~executions.NebulaNodeExecution

"""

from nebulakit.remote.entities import (
    NebulaBranchNode,
    NebulaLaunchPlan,
    NebulaNode,
    NebulaTask,
    NebulaTaskNode,
    NebulaWorkflow,
    NebulaWorkflowNode,
)
from nebulakit.remote.executions import NebulaNodeExecution, NebulaTaskExecution, NebulaWorkflowExecution
from nebulakit.remote.remote import NebulaRemote
