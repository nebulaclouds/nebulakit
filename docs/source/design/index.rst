.. _design:

########
Overview
########

Nebulakit is comprised of a handful of different logical components, each discusssed in greater detail below:

* :ref:`Models Files <design-models>` - These are almost Protobuf generated files.
* :ref:`Authoring <design-authoring>` - This provides the core Nebula authoring experiences, allowing users to write tasks, workflows, and launch plans.
* :ref:`Control Plane <design-control-plane>` - The code here allows users to interact with the control plane through Python objects.
* :ref:`Execution <design-execution>` - A small shim layer basically that handles interaction with the Nebula ecosystem at execution time.
* :ref:`CLIs and Clients <design-clis>` - Command line tools users may interact with, and the control plane client the CLIs call.

.. toctree::
   :maxdepth: 1
   :caption: Structure and Layout of Nebulakit
   :hidden:

   models
   authoring
   Control Plane: NebulaRemote <control_plane>
   execution
   clis
