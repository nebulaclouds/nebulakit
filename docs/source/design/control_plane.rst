.. _design-control-plane:

###################################################
NebulaRemote: A Programmatic Control Plane Interface
###################################################

.. tags:: Remote, Basic

For those who require programmatic access to the control plane, the :mod:`~nebulakit.remote` module enables you to perform
certain operations in a Python runtime environment.

Since this section naturally deals with the control plane, this discussion is only relevant for those who have a Nebula
backend set up and have access to it (a local demo cluster will suffice as well).

*****************************
Creating a NebulaRemote Object
*****************************

The :class:`~nebulakit.remote.remote.NebulaRemote` class is the entrypoint for programmatically performing operations in a Python
runtime. It can be initialized by passing in the:

* :py:class:`~nebulakit.configuration.Config` object: the parent configuration object that holds all the configuration information to connect to the Nebula backend.
* :py:attr:`~nebulakit.remote.remote.NebulaRemote.default_project`: the default project to use when fetching or executing nebula entities.
* :py:attr:`~nebulakit.remote.remote.NebulaRemote.default_domain`: the default domain to use when fetching or executing nebula entities.
* :py:attr:`~nebulakit.remote.remote.NebulaRemote.file_access`: the file access provider to use for offloading non-literal inputs/outputs.
* ``kwargs``: additional arguments that need to be passed to create ``SynchronousNebulaClient``.

A :class:`~nebulakit.remote.remote.NebulaRemote` object can be created in various ways:

Auto
====

The :py:class:`~nebulakit.configuration.Config` class's :py:meth:`~nebulakit.configuration.Config.auto` method can be used to automatically
construct the ``Config`` object.

.. code-block:: python

    from nebulakit.remote import NebulaRemote
    from nebulakit.configuration import Config

    remote = NebulaRemote(config=Config.auto())

``auto`` also accepts a ``config_file`` argument, which is the path to the configuration file to use.
The order of precedence that ``auto`` follows is:

* Finds all the environment variables that match the configuration variables.
* If no environment variables are set, it looks for a configuration file at the path specified by the ``config_file`` argument.
* If no configuration file is found, it uses the default values.

Sandbox
=======

The :py:class:`~nebulakit.configuration.Config` class's :py:meth:`~nebulakit.configuration.Config.for_sandbox` method can be used to
construct the ``Config`` object, specifically to connect to the Nebula cluster.

.. code-block:: python

    from nebulakit.remote import NebulaRemote
    from nebulakit.configuration import Config

    remote = NebulaRemote(config=Config.for_sandbox())

The initialization is as simple as calling ``for_sandbox()`` on the ``Config`` class!
This, by default, uses ``localhost:30081`` as the endpoint, and the default minio credentials.

If the sandbox is in a hosted-like environment, then *port-forward* or *ingress URLs* need to be taken care of.

Any Endpoint
============

The :py:class:`~nebulakit.configuration.Config` class's :py:meth:`~nebulakit.configuration.Config.for_endpoint` method can be used to
construct the ``Config`` object to connect to a specific endpoint.

.. code-block:: python

    from nebulakit.remote import NebulaRemote
    from nebulakit.configuration import Config

    remote = NebulaRemote(
        config=Config.for_endpoint(endpoint="nebula.example.net"),
        default_project="nebulasnacks",
        default_domain="development",
    )

The ``for_endpoint`` method also accepts:

* ``insecure``: whether to use insecure connections. Defaults to ``False``.
* ``data_config``: can be used to configure how data is downloaded or uploaded to a specific blob storage like S3, GCS, etc.
* ``config_file``: the path to the configuration file to use.

.. _general_initialization:

Generalized Initialization
==========================

The :py:class:`~nebulakit.configuration.Config` class can be directly used to construct the ``Config`` object if additional configuration is needed.
You can send :py:class:`~nebulakit.configuration.PlatformConfig`, :py:class:`~nebulakit.configuration.DataConfig`,
:py:class:`~nebulakit.configuration.SecretsConfig`, and :py:class:`~nebulakit.configuration.StatsConfig` objects to the ``Config`` class.

.. list-table:: ``Config`` Attributes
   :widths: 50 50

   * - ``PlatformConfig``
     - Settings to talk to a Nebula backend.
   * - ``DataConfig``
     - Any data storage specific configuration.
   * - ``SecretsConfig``
     - Configuration for secrets.
   * - ``StatsConfig``
     - Configuration for sending statsd.

For example:

.. code-block:: python

    from nebulakit.remote import NebulaRemote
    from nebulakit.configuration import Config, PlatformConfig

    remote = NebulaRemote(
        config=Config(
            platform=PlatformConfig(
                endpoint="nebula.example.net",
                insecure=False,
                client_id="my-client-id",
                client_credentials_secret="my-client-secret",
                auth_mode="client_credentials",
            ),
            secrets=SecretsConfig(default_dir="/etc/secrets"),
        )
    )

*****************
Fetching Entities
*****************

Tasks, workflows, launch plans, and executions can be fetched using NebulaRemote.

.. code-block:: python

    nebula_task = remote.fetch_task(name="my_task", version="v1")
    nebula_workflow = remote.fetch_workflow(name="my_workflow", version="v1")
    nebula_launch_plan = remote.fetch_launch_plan(name="my_launch_plan", version="v1")
    nebula_execution = remote.fetch_execution(name="my_execution")

``project`` and ``domain`` can also be specified in all the ``fetch_*`` calls.
If not specified, the default values given during the creation of the NebulaRemote object will be used.

The following is an example that fetches :py:func:`~nebulakit.task`s and creates a :py:func:`~nebulakit.workflow`:

.. code-block:: python

    from nebulakit import workflow

    task_1 = remote.fetch_task(name="core.basic.hello_world.say_hello", version="v1")
    task_2 = remote.fetch_task(
        name="core.basic.lp.greet",
        version="v13",
        project="nebulasnacks",
        domain="development",
    )


    @workflow
    def my_remote_wf(name: str) -> int:
        return task_2(task_1(name=name))

Another example that dynamically creates a launch plan for the ``my_remote_wf`` workflow:

.. code-block:: python

    from nebulakit import LaunchPlan

    nebula_workflow = remote.fetch_workflow(
        name="my_workflow", version="v1", project="nebulasnacks", domain="development"
    )
    launch_plan = LaunchPlan.get_or_create(name="my_launch_plan", workflow=nebula_workflow)

********************
Registering Entities
********************

Tasks, workflows, and launch plans can be registered using NebulaRemote.

.. code-block:: python

    from nebulakit.configuration import SerializationSettings

    nebula_entity = ...
    nebula_task = remote.register_task(
        entity=nebula_entity,
        serialization_settings=SerializationSettings(image_config=None),
        version="v1",
    )
    nebula_workflow = remote.register_workflow(
        entity=nebula_entity,
        serialization_settings=SerializationSettings(image_config=None),
        version="v1",
    )
    nebula_launch_plan = remote.register_launch_plan(entity=nebula_entity, version="v1")

* ``entity``: the entity to register.
* ``version``: the version that will be used to register. If not specified, the version used in serialization settings will be used.
* ``serialization_settings``: the serialization settings to use. Refer to :py:class:`~nebulakit.configuration.SerializationSettings` to know all the acceptable parameters.

All the additional parameters which can be sent to the ``register_*`` methods can be found in the documentation for the corresponding method:
:py:meth:`~nebulakit.remote.remote.NebulaRemote.register_task`, :py:meth:`~nebulakit.remote.remote.NebulaRemote.register_workflow`,
and :py:meth:`~nebulakit.remote.remote.NebulaRemote.register_launch_plan`.

The :py:class:`~nebulakit.configuration.SerializationSettings` class accepts :py:class:`~nebulakit.configuration.ImageConfig` which
holds the available images to use for the registration.

The following example showcases how to register a workflow using an existing image if the workflow is created locally:

.. code-block:: python

    from nebulakit.configuration import ImageConfig

    img = ImageConfig.from_images(
        "docker.io/xyz:latest", {"spark": "docker.io/spark:latest"}
    )
    wf2 = remote.register_workflow(
        my_remote_wf,
        serialization_settings=SerializationSettings(image_config=img),
        version="v1",
    )

******************
Executing Entities
******************

You can execute a task, workflow, or launch plan using :meth:`~nebulakit.remote.remote.NebulaRemote.execute` method
which returns a :class:`~nebulakit.remote.executions.NebulaWorkflowExecution` object.
For more information on Nebula entities, see the :ref:`remote nebula entities <remote-nebula-execution-objects>` reference.

.. code-block:: python

    nebula_entity = ...  # one of NebulaTask, NebulaWorkflow, or NebulaLaunchPlan
    execution = remote.execute(
        nebula_entity, inputs={...}, execution_name="my_execution", wait=True
    )

* ``inputs``: the inputs to the entity.
* ``execution_name``: the name of the execution. This is useful to avoid de-duplication of executions.
* ``wait``: synchronously wait for the execution to complete.

Additional arguments include:

* ``project``: the project on which to execute the entity.
* ``domain``: the domain on which to execute the entity.
* ``type_hints``: a dictionary mapping Python types to their corresponding Nebula types.
* ``options``: options can be configured for a launch plan during registration or overriden during execution. Refer to :py:class:`~nebulakit.remote.remote.Options` to know all the acceptable parameters.

The following is an example demonstrating how to use the :py:class:`~nebulakit.remote.remote.Options` class to configure a Nebula entity:

.. code-block:: python

    from nebulakit.models.common import AuthRole, Labels
    from nebulakit.tools.translator import Options

    nebula_entity = ...  # one of NebulaTask, NebulaWorkflow, or NebulaLaunchPlan
    execution = remote.execute(
        nebula_entity,
        inputs={...},
        execution_name="my_execution",
        wait=True,
        options=Options(
            raw_data_prefix="s3://my-bucket/my-prefix",
            auth_role=AuthRole(assumable_iam_role="my-role"),
            labels=Labels({"my-label": "my-value"}),
        ),
    )

**********************************
Retrieving & Inspecting Executions
**********************************

After an execution is completed, you can retrieve the execution using the :meth:`~nebulakit.remote.remote.NebulaRemote.fetch_execution` method.
The fetched execution can be used to retrieve the inputs and outputs of an execution.

.. code-block:: python

    execution = remote.fetch_execution(
        name="fb22e306a0d91e1c6000", project="nebulasnacks", domain="development"
    )
    input_keys = execution.inputs.keys()
    output_keys = execution.outputs.keys()

The ``inputs`` and ``outputs`` correspond to the top-level execution or the workflow itself.

To fetch a specific output, say, a model file:

.. code-block:: python

    model_file = execution.outputs["model_file"]
    with open(model_file) as f:
        # use mode
        ...

You can use :meth:`~nebulakit.remote.remote.NebulaRemote.sync` to sync the entity object's state with the remote state during the execution run:

.. code-block:: python

    synced_execution = remote.sync(execution, sync_nodes=True)
    node_keys = synced_execution.node_executions.keys()

.. note::

    During the sync, you may come across ``Received message larger than max (xxx vs. 4194304)`` error if the message size is too large. In that case, edit the ``nebula-admin-base-config`` config map using the command ``kubectl edit cm nebula-admin-base-config -n nebula`` to increase the ``maxMessageSizeBytes`` value. Refer to the :ref:`troubleshooting guide <troubleshoot>` in case you've queries about the command's usage.

``node_executions`` will fetch all the underlying node executions recursively.

To fetch output of a specific node execution:

.. code-block:: python

    node_execution_output = synced_execution.node_executions["n1"].outputs["model_file"]

:ref:`Node <nebula:divedeep-nodes>` here, can correspond to a task, workflow, or branch node.

****************
Listing Entities
****************

To list the recent executions, use the :meth:`~nebulakit.remote.remote.NebulaRemote.recent_executions` method.

.. code-block:: python

    recent_executions = remote.recent_executions(project="nebulasnacks", domain="development", limit=10)

The ``limit`` parameter is optional and defaults to 100.

To list tasks by version, use the :meth:`~nebulakit.remote.remote.NebulaRemote.list_tasks_by_version` method.

.. code-block:: python

    tasks = remote.list_tasks_by_version(project="nebulasnacks", domain="development", version="v1")

************************
Terminating an Execution
************************

To terminate an execution, use the :meth:`~nebulakit.remote.remote.NebulaRemote.terminate` method.

.. code-block:: python

    execution = remote.fetch_execution(name="fb22e306a0d91e1c6000", project="nebulasnacks", domain="development")
    remote.terminate(execution, cause="Code needs to be updated")
