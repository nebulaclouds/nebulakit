from nebulaidl.admin import task_execution_pb2 as _task_execution_pb2

from nebulakit.models import common as _common
from nebulakit.models.core import execution as _execution
from nebulakit.models.core import identifier as _identifier


class TaskExecutionClosure(_common.NebulaIdlEntity):
    def __init__(
        self,
        phase,
        logs,
        started_at,
        duration,
        created_at,
        updated_at,
        output_uri=None,
        error=None,
    ):
        """
        :param int phase: Enum value from nebulakit.models.core.execution.TaskExecutionPhase
        :param list[nebulakit.models.core.execution.TaskLog] logs: List of all logs associated with the execution.
        :param datetime.datetime started_at:
        :param datetime.timedelta duration:
        :param datetime.datetime created_at:
        :param datetime.datetime updated_at:
        :param Text output_uri: If task is successful and in terminal state, this will be the path to the output
            literals.
        :param nebulakit.models.core.execution.ExecutionError error: If task has failed and in terminal state, this will
            be set to the error encountered.
        """
        self._phase = phase
        self._logs = logs
        self._started_at = started_at
        self._duration = duration
        self._created_at = created_at
        self._updated_at = updated_at
        self._output_uri = output_uri
        self._error = error

    @property
    def phase(self):
        """
        Enum value from nebulakit.models.core.execution.TaskExecutionPhase
        :rtype: int
        """
        return self._phase

    @property
    def logs(self):
        """
        :rtype: list[nebulakit.models.core.execution.TaskLog]
        """
        return self._logs

    @property
    def started_at(self):
        """
        :rtype: datetime.datetime
        """
        return self._started_at

    @property
    def created_at(self):
        """
        :rtype: datetime.datetime
        """
        return self._created_at

    @property
    def updated_at(self):
        """
        :rtype: datetime.datetime
        """
        return self._updated_at

    @property
    def duration(self):
        """
        :rtype: datetime.timedelta
        """
        return self._duration

    @property
    def output_uri(self):
        """
        :rtype: Text
        """
        return self._output_uri

    @property
    def error(self):
        """
        :rtype: nebulakit.models.core.execution.ExecutionError
        """
        return self._error

    def to_nebula_idl(self):
        """
        :rtype: nebulaidl.admin.task_execution_pb2.TaskExecutionClosure
        """
        p = _task_execution_pb2.TaskExecutionClosure(
            phase=self.phase,
            logs=[l.to_nebula_idl() for l in self.logs],
            output_uri=self.output_uri,
            error=self.error.to_nebula_idl() if self.error is not None else None,
        )
        p.started_at.FromDatetime(self.started_at)
        p.created_at.FromDatetime(self.created_at)
        p.updated_at.FromDatetime(self.updated_at)
        p.duration.FromTimedelta(self.duration)
        return p

    @classmethod
    def from_nebula_idl(cls, p):
        """
        :param nebulaidl.admin.task_execution_pb2.TaskExecutionClosure p:
        :rtype: TaskExecutionClosure
        """
        return cls(
            phase=p.phase,
            logs=[_execution.TaskLog.from_nebula_idl(l) for l in p.logs],
            output_uri=p.output_uri if p.HasField("output_uri") else None,
            error=_execution.ExecutionError.from_nebula_idl(p.error) if p.HasField("error") else None,
            started_at=p.started_at.ToDatetime(),
            created_at=p.created_at.ToDatetime(),
            updated_at=p.updated_at.ToDatetime(),
            duration=p.duration.ToTimedelta(),
        )


class TaskExecution(_common.NebulaIdlEntity):
    def __init__(self, id, input_uri, closure, is_parent):
        """
        :param nebulakit.models.core.identifier.TaskExecutionIdentifier id:
        :param Text input_uri:
        :param TaskExecutionClosure closure:
        :param bool is_parent:
        """
        self._id = id
        self._input_uri = input_uri
        self._closure = closure
        self._is_parent = is_parent

    @property
    def id(self):
        """
        :rtype: nebulakit.models.core.identifier.TaskExecutionIdentifier
        """
        return self._id

    @property
    def input_uri(self):
        """
        :rtype: Text
        """
        return self._input_uri

    @property
    def closure(self):
        """
        :rtype: TaskExecutionClosure
        """
        return self._closure

    @property
    def is_parent(self):
        """
        :rtype: bool
        """
        return self._is_parent

    def to_nebula_idl(self):
        """
        :rtype: nebulaidl.admin.task_execution_pb2.TaskExecution
        """
        return _task_execution_pb2.TaskExecution(
            id=self.id.to_nebula_idl(),
            input_uri=self.input_uri,
            closure=self.closure.to_nebula_idl(),
            is_parent=self.is_parent,
        )

    @classmethod
    def from_nebula_idl(cls, proto):
        """
        :param nebulaidl.admin.task_execution_pb2.TaskExecution proto:
        :rtype: TaskExecution
        """
        return cls(
            id=_identifier.TaskExecutionIdentifier.from_nebula_idl(proto.id),
            input_uri=proto.input_uri,
            closure=TaskExecutionClosure.from_nebula_idl(proto.closure),
            is_parent=proto.is_parent,
        )
