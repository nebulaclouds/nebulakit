from nebulaidl.core import compiler_pb2 as _compiler_pb2

from nebulakit.models import common as _common
from nebulakit.models.core import workflow as _core_workflow_models


class ConnectionSet(_common.NebulaIdlEntity):
    class IdList(_common.NebulaIdlEntity):
        def __init__(self, ids):
            """
            :param list[Text] ids:
            """
            self._ids = ids

        @property
        def ids(self):
            """
            :rtype: list[Text]
            """
            return self._ids

        def to_nebula_idl(self):
            """
            :rtype: nebulaidl.core.compiler_pb2.ConnectionSet.IdList
            """
            return _compiler_pb2.ConnectionSet.IdList(ids=self.ids)

        @classmethod
        def from_nebula_idl(cls, p):
            """
            :param nebulaidl.core.compiler_pb2.ConnectionSet.IdList p:
            :rtype: ConnectionSet.IdList
            """
            return cls(p.ids)

    def __init__(self, upstream, downstream):
        """
        :param dict[Text, ConnectionSet.IdList] upstream:
        :param dict[Text, ConnectionSet.IdList] downstream:
        """
        self._upstream = upstream
        self._downstream = downstream

    @property
    def upstream(self):
        """
        :rtype: dict[Text, ConnectionSet.IdList]
        """
        return self._upstream

    @property
    def downstream(self):
        """
        :rtype: dict[Text, ConnectionSet.IdList]
        """
        return self._downstream

    def to_nebula_idl(self):
        """
        :rtype: nebulaidl.core.compiler_pb2.ConnectionSet
        """
        return _compiler_pb2.ConnectionSet(
            upstream={k: v.to_nebula_idl() for k, v in self.upstream.items()},
            downstream={k: v.to_nebula_idl() for k, v in self.upstream.items()},
        )

    @classmethod
    def from_nebula_idl(cls, p):
        """
        :param nebulaidl.core.compiler_pb2.ConnectionSet p:
        :rtype: ConnectionSet
        """
        return cls(
            upstream={k: ConnectionSet.IdList.from_nebula_idl(v) for k, v in p.upstream.items()},
            downstream={k: ConnectionSet.IdList.from_nebula_idl(v) for k, v in p.downstream.items()},
        )


class CompiledWorkflow(_common.NebulaIdlEntity):
    def __init__(self, template, connections):
        """
        :param nebulakit.models.core.workflow.WorkflowTemplate template:
        :param ConnectionSet connections:
        """
        self._template = template
        self._connections = connections

    @property
    def template(self):
        """
        :rtype: nebulakit.models.core.workflow.WorkflowTemplate
        """
        return self._template

    @property
    def connections(self):
        """
        :rtype: ConnectionSet
        """
        return self._connections

    def to_nebula_idl(self):
        """
        :rtype: nebulaidl.core.compiler_pb2.CompiledWorkflow
        """
        return _compiler_pb2.CompiledWorkflow(
            template=self.template.to_nebula_idl(),
            connections=self.connections.to_nebula_idl(),
        )

    @classmethod
    def from_nebula_idl(cls, p):
        """
        :param nebulaidl.core.compiler_pb2.CompiledWorkflow p:
        :rtype: CompiledWorkflow
        """
        return cls(
            template=_core_workflow_models.WorkflowTemplate.from_nebula_idl(p.template),
            connections=ConnectionSet.from_nebula_idl(p.connections),
        )


# TODO: properly sort out the model code and remove one of these duplicate CompiledTasks
class CompiledTask(_common.NebulaIdlEntity):
    def __init__(self, template):
        """
        :param TODO template:
        """
        self._template = template

    @property
    def template(self):
        """
        :rtype: TODO
        """
        return self._template

    def to_nebula_idl(self):
        """
        :rtype: nebulaidl.core.compiler_pb2.CompiledTask
        """
        return _compiler_pb2.CompiledTask(template=self.template)  # TODO: .to_nebula_idl()

    @classmethod
    def from_nebula_idl(cls, p):
        """
        :param nebulaidl.core.compiler_pb2.CompiledTask p:
        :rtype: CompiledTask
        """
        # TODO: Refactor task so we don't have cyclical import
        return cls(None)


class CompiledWorkflowClosure(_common.NebulaIdlEntity):
    def __init__(self, primary, sub_workflows, tasks):
        """
        :param CompiledWorkflow primary:
        :param list[CompiledWorkflow] sub_workflows:
        :param list[CompiledTask] tasks:
        """
        self._primary = primary
        self._sub_workflows = sub_workflows
        self._tasks = tasks

    @property
    def primary(self):
        """
        :rtype: CompiledWorkflow
        """
        return self._primary

    @property
    def sub_workflows(self):
        """
        :rtype: list[CompiledWorkflow]
        """
        return self._sub_workflows

    @property
    def tasks(self):
        """
        :rtype: list[CompiledTask]
        """
        return self._tasks

    def to_nebula_idl(self):
        """
        :rtype: nebulaidl.core.compiler_pb2.CompiledWorkflowClosure
        """
        return _compiler_pb2.CompiledWorkflowClosure(
            primary=self.primary.to_nebula_idl(),
            sub_workflows=[s.to_nebula_idl() for s in self.sub_workflows],
            tasks=[t.to_nebula_idl() for t in self.tasks],
        )

    @classmethod
    def from_nebula_idl(cls, p):
        """
        :param nebulaidl.core.compiler_pb2.CompiledWorkflowClosure p:
        :rtype: CompiledWorkflowClosure
        """
        # This import is here to prevent a circular dependency issue.
        # TODO: properly sort out the model code and remove the duplicate CompiledTask
        from nebulakit.models.task import CompiledTask as _CompiledTask

        return cls(
            primary=CompiledWorkflow.from_nebula_idl(p.primary),
            sub_workflows=[CompiledWorkflow.from_nebula_idl(s) for s in p.sub_workflows],
            tasks=[_CompiledTask.from_nebula_idl(t) for t in p.tasks],
        )
