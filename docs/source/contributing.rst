.. _contributing:

###########################
Nebulakit Contribution Guide
###########################

.. tags:: Contribute, Basic

First off, thank you for thinking about contributing! Below you'll find instructions that will hopefully guide you through how to fix, improve, and extend Nebulakit.

Please also take some time to read through the :std:ref:`design guides <design>`, which describe the various parts of Nebulakit and should make contributing easier.

*******************
📜 Background
*******************

Below is a listing of the most important packages that comprise the nebulakit SDK:

- ``nebulakit/core``
  This holds all the core functionality of the new API.
- ``nebulakit/types``
  We bundle some special types like ``NebulaFile, NebulaSchema etc`` by default here.
- ``nebulakit/extend``
  This is the future home of extension points, and currently serves as the raw documentation for extensions.
- ``nebulakit/extras``
  This contains code that we want bundled with Nebulakit but not everyone may find useful (for example AWS and GCP
  specific logic).
- ``nebulakit/remote``
  This implements the interface to interact with the Nebula service. Think of the code here as the Python-object version of Console.
- ``nebulakit/testing``
  is the future home for testing functionality like ``mock`` etc, and currently serves as documentation.
  All test extensions should be imported from here.
- ``nebulakit/models``
  Protobuf generated Python code is not terribly user-friendly, so we improve upon those ``nebulaidl`` classes here.
- ``plugins``
  is the source of all plugins
- ``nebulakit/bin/entrypoint.py``
  The run time entrypoint for nebulakit. When a task kicks off, this is where the click command goes.
- ``nebulakit/clis``
  This is the home for the CLIs.
- ``nebulakit/configuration``
  This holds all the configuration objects, but dependency on configuration should be carefully considered as it
  makes compiled Nebula tasks and workflows less portable (i.e. if you run ``pynebula package`` can someone else use
  those serialized objects).

Please also see the :std:ref:`design overview section <design>` for more in-depth information.


******************
💻 Contribute Code
******************

Setup (Do Once)
===============

We recommend using a virtual environment to develop Nebulakit. Inside the top level Nebulakit repo folder, run: ::

    virtualenv ~/.virtualenvs/nebulakit
    source ~/.virtualenvs/nebulakit/bin/activate
    make setup

This will install Nebulakit dependencies and Nebulakit in editable mode. This links your virtual Python's ``site-packages`` with your local repo folder, allowing your local changes to take effect when the same Python interpreter runs ``import nebulakit``.

Plugin Development
==================

As discussed in the design component, Nebulakit plugins currently live in this Nebulakit repo, but under a different top level folder ``plugins``.
In the future, this will be separated out into a different repo. These plugins follow a `microlib <https://medium.com/@jherreras/python-microlibs-5be9461ad979>`__ structure, which will persist even if we move repos. ::

    source ~/.virtualenvs/nebulakit/bin/activate
    cd plugins
    pip install -e .

This should install all the plugins in editable mode as well.

Iteration
=========

Make
^^^^
Some helpful make commands ::

    $ make
      setup        Install requirements
      fmt          Format code with ruff
      lint         Run linters
      test         Run tests
      requirements Compile requirements

Testing
^^^^^^^
Three levels of testing are available.

Unit Testing
------------
Running unit tests: ::

    source ~/.virtualenvs/nebulakit/bin/activate
    make test

Cookbook Testing
----------------
Please see the `cookbook <https://github.com/nebulaclouds/nebulasnacks/tree/master/cookbook>`__ and the generated `docs <https://nebulacookbook.readthedocs.io/en/latest/>`__ for more information.
This example repo can be cloned and run on a local Nebula cluster, or just in your IDE or other Python environment.

Follow the setup instructions for the cookbook and then override it with the version of Nebulakit you're interested in testing by running something like: ::

    pip install https://github.com/nebulaclouds/nebulakit/archive/a32ab82bef4d9ff53c2b7b4e69ff11f1e93858ea.zip#egg=nebulakit
    # Or for a plugin
    pip install https://github.com/nebulaclouds/nebulakit/archive/e128f66dda48bbfc6076d240d39e4221d6af2d2b.zip#subdirectory=plugins/pod&egg=nebulakitplugins-pod

Change the actual link to be from your fork if you are using a fork.

End-to-end Testing
------------------

.. TODO: Replace this with actual instructions

The Nebula developer experience team has put together an end-to-end testing framework that will spin up a K8s cluster, install Nebula onto it, and run through a series of workflows.
Please contact us if you reach this stage and would like more information on this.


Pre-commit hooks
================

We use `pre-commit <https://pre-commit.com/>`__ to automate linting and code formatting on every commit.
Configured hooks include `ruff <https://github.com/astral-sh/ruff>`__ and also linters to check for the validity of YAML files and ensuring that newlines are added to the end of files.

We run all those hooks in CI, but if you want to run them locally on every commit, run `pre-commit install` after installing the dev environment requirements. In case you want to disable `pre-commit` hooks locally, for example, while you're iterating on some feature, run `pre-commit uninstall`. More info in https://pre-commit.com/.


Formatting
==========

We use `ruff <https://github.com/astral-sh/ruff>`__  to autoformat code. In fact, they have been configured as git hooks in `pre-commit`. Run the following commands to execute the formatters. ::

    source ~/.virtualenvs/nebulakit/bin/activate
    make fmt

Spell-checking
==============

We use `codespell <https://github.com/codespell-project/codespell>`__ to catch spelling mistakes in both code and documentation. Run the following commands to spell-check changes. ::

    source ~/.virtualenvs/nebulakit/bin/activate
    make spellcheck

******************************
📃 Contribute to Documentation
******************************

1. Install requirements by running ``make doc-requirements.txt`` in the root of the repo
2. Make the required changes
3. Verify if the documentation looks as expected by running ``make html`` in the `docs <https://github.com/nebulaclouds/nebulakit/tree/master/docs>`__ directory
4. Open HTML pages present in the ``docs/build`` directory in the browser
5. After creating the pull request, check if the docs are rendered correctly by clicking on the documentation check

   .. image:: https://raw.githubusercontent.com/nebulaclouds/static-resources/main/common/test_docs_link.png
       :alt: Doc link in PR

**********************************
📝 Releases and Project Management
**********************************

Currently, Nebulakit and all its plugins share one common version.
To release, contact a member of the Nebulakit repo maintainers or committers, and request a release.
We will create a GitHub release off of master, which will automatically publish a Pypi package.
