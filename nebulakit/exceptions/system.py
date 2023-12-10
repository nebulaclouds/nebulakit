from nebulakit.exceptions import base as _base_exceptions


class NebulaSystemException(_base_exceptions.NebulaRecoverableException):
    _ERROR_CODE = "SYSTEM:Unknown"


class NebulaNotImplementedException(NebulaSystemException, NotImplementedError):
    _ERROR_CODE = "SYSTEM:NotImplemented"


class NebulaEntrypointNotLoadable(NebulaSystemException):
    _ERROR_CODE = "SYSTEM:UnloadableCode"

    @classmethod
    def _create_verbose_message(cls, task_module, task_name=None, additional_msg=None):
        if task_name is None:
            return "Entrypoint is not loadable!  Could not load the module: '{task_module}'{additional_msg}".format(
                task_module=task_module,
                additional_msg=" due to error: {}".format(additional_msg) if additional_msg is not None else ".",
            )
        else:
            return (
                "Entrypoint is not loadable!  Could not find the task: '{task_name}' in '{task_module}'"
                "{additional_msg}".format(
                    task_module=task_module,
                    task_name=task_name,
                    additional_msg="." if additional_msg is None else " due to error: {}".format(additional_msg),
                )
            )

    def __init__(self, task_module, task_name=None, additional_msg=None):
        super(NebulaSystemException, self).__init__(
            self._create_verbose_message(task_module, task_name=task_name, additional_msg=additional_msg)
        )


class NebulaSystemAssertion(NebulaSystemException, AssertionError):
    _ERROR_CODE = "SYSTEM:AssertionError"


class NebulaAgentNotFound(NebulaSystemException, AssertionError):
    _ERROR_CODE = "SYSTEM:AgentNotFound"
