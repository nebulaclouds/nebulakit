.. _design-execution:

#######################
Execution Time Support
#######################

.. tags:: Design, Basic

Most of the tasks that are written in Nebulakit will be Python functions decorated with ``@task`` which turns the body of the function into a Nebula task, capable of being run independently, or included in any number of workflows. The interaction between Nebulakit and these tasks do not end once they have been serialized and registered onto the Nebula control plane however. When compiled, the command that will be executed when the task is run is hardcoded into the task definition itself.

In the basic ``@task`` decorated function scenario, the command to be run will be something containing ``pynebula-execute``, which is one of the CLIs discussed in that section.

That command, if you were to inspect a serialized task, might look something like ::

    nebulakit_venv pynebula-execute --task-module app.workflows.failing_workflows --task-name divider --inputs {{.input}} --output-prefix {{.outputPrefix}} --raw-output-data-prefix {{.rawOutputDataPrefix}}

The point of running this script, or rather the reason for having any Nebula-related logic at execution time, is purely to codify and streamline the interaction between Nebula the platform, and the function body comprising user code. The Nebula CLI is responsible for:

* I/O: The templated ``--inputs`` and ``--output-prefix`` arguments in the example command above will be filled in by the Nebula execution engine with S3 path (in the case of an AWS deployment). The ``pynebula`` script will download the inputs to the right location in the container, and upload the results to the ``output-prefix`` location.
* Ensure that raw output data prefix configuration option, which is again filled in by the Nebula engine, is respected so that ``NebulaFile``, ``NebulaDirectory``, and ``NebulaSchema`` objects offload their data to the correct place.
* Capture and handle error reporting: Exceptions thrown in the course of task execution are captured and uploaded to the Nebula control plane for display on the Console.
* Set up helper utilities like the ``statsd`` handle, logging and logging levels, etc.
* Ensure configuration options about the Nebula backend, which are passed through by the Nebula engine, are properly loaded in Python memory.
