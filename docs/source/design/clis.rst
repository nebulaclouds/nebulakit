.. _design-clis:

###################################
Command Line Interfaces and Clients
###################################

.. tags:: CLI, Basic

Nebulakit currently ships with two CLIs, both of which rely on the same client implementation code.

*******
Clients
*******
The client code is located in ``nebulakit/clients`` and there are two.

* Similar to the :ref:`design-models` files, but a bit more complex, the ``raw`` one is basically a wrapper around the protobuf generated code, with some handling for authentication in place, and acts as a mechanism for autocompletion and comments.
* The ``friendly`` client uses the ``raw`` client, adds handling of things like pagination, and is structurally more aligned with the functionality and call pattern of the CLI itself.

:py:class:`clients.friendly.SynchronousNebulaClient`

:py:class:`clients.raw.RawSynchronousNebulaClient`

***********************
Command Line Interfaces
***********************

Nebulactl
=========

`Nebulactl <https://pypi.org/project/yt-nebula-playground-nebulactl/>`__ is the general CLI to communicate with the Nebula control plane (NebulaAdmin). Think of this as the ``kubectl`` for Nebula.

Think of this as a network-aware (can talk to NebulaAdmin) but not code-aware (no need to have user code checked out) CLI. In the registration flow, this CLI is responsible for shipping the compiled Protobuf files off to NebulaAdmin.

Pynebula
========

Unlike ``nebulactl``, think of this CLI as code-aware, which is responsible for the serialization (compilation) step in the registration flow. It will parse through the user code, looking for tasks, workflows, and launch plans, and compile them to `protobuf files <https://github.com/nebulaclouds/nebulaidl/blob/0b20c5c99f9e964370d4f4ca663990ed56a14c7c/protos/nebulaidl/core/workflow_closure.proto#L11-L18>`__.

.. _pynebula-run:

What is ``pynebula run``?
========================

The ``pynebula run`` command is a light-weight, convenience command that incorporates packaging, registering, and launching a workflow into a single command.

It is not a fully featured production scale mode of operation, because it is designed to be a quick and easy iteration tool to get started with Nebula or test small self-contained scripts. The caveat here is it operates on a single file, and this file will have to contain all the required Nebula entities. Let’s take an example so that you can understand it better.

Suppose you execute a script that defines 10 tasks and a workflow that calls only 2 out of the 10 tasks. The remaining 8 tasks don’t get registered at that point.

It is considered fast registration because when a script is executed using ``pynebula run``, the script is bundled up and uploaded to NebulaAdmin. When the task is executed in the backend, this zipped file is extracted and used.

.. _pynebula-register:

What is ``pynebula register``?
=============================

``pynebula register`` is a command that registers all the workflows present in the repository/directory using fast-registration. It is equivalent to using two commands (``pynebula package`` and ``nebulactl register``) to perform the same operation (registration). It compiles the Python code into protobuf objects and uploads the files directly to NebulaAdmin. In the process, the protobuf objects are not written to the local disk, making it difficult to introspect these objects since they are lost.

The ``pynebula package`` command parses and compiles the user’s Python code into Nebula protobuf objects. These compiled objects are stored as protobuf files and are available locally after you run the ``pynebula package``.

The ``nebulactl register`` command then ships the protobuf objects over the network to the Nebula control plane. In the process, ``nebulactl`` also allows you to set run-time attributes such as IAM roles, K8s service accounts, etc.

``pynebula package + nebulactl register`` produces a **portable** package (a .tgz file) of Nebula entities (compiled protobuf files that are stored on the local disk), which makes it easy to introspect the objects at a later time if required. You can use register this package with multiple Nebula backends. You can save this package, use it for an audit, register with different NebulaAdmins, etc.

Why should you use ``pynebula register``?
========================================

The ``pynebula register`` command bridges the gap between ``pynebula package`` + ``nebulactl register`` and ``pynebula run`` commands. It offers the functionality of the ``pynebula package`` (with smarter naming semantics and combining the network call into one step).

.. note ::

   You can't use ``pynebula register`` if you are unaware of the run-time options yet (IAM role, service account, and so on).

Usage
=====

.. prompt:: bash $

  pynebula register --image ghcr.io/nebulaclouds/nebulacookbook:core-latest --image trainer=ghcr.io/nebulaclouds/nebulacookbook:core-latest --image predictor=ghcr.io/nebulaclouds/nebulacookbook:core-latest --raw-data-prefix s3://development-service-nebula/reltsts nebula_basics

In a broad way, ``pynebula register`` is equivalent to ``pynebula run`` minus launching workflows, with the exception that ``pynebula run`` can only register a single workflow, whereas ``pynebula register`` can register all workflows in a repository.

What is the difference between ``pynebula package + nebulactl register`` and ``pynebula register``?
================================================================================================

``pynebula package + nebulactl register`` works well with multiple NebulaAdmins since it produces a portable package. You can also use it to run scripts in CI.

``pynebula register`` works well in single NebulaAdmin use-cases and cases where you are iterating locally.

Should you use ``pynebula run`` or ``pynebula package + nebulactl register``?
==========================================================================

Both the commands have their own place in a production Nebula setting.

``pynebula run`` is useful when you are getting started with Nebula, testing small scripts, or iterating over local scripts.

``pynebula package + nebulactl register`` is useful when you wish to work with multiple NebulaAdmins, wherein you can package the script, compile it into protobuf objects, write it to local disk, and upload this zipped package to different NebulaAdmins.

.. note ::

   Neither ``pynebula register`` nor ``pynebula run`` commands work on Python namespace packages since both the tools traverse the filesystem to find the first folder that doesn't have an __init__.py file, which is interpreted as the root of the project. Both the commands use this root as the basis to name the Nebula entities.
