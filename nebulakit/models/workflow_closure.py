from nebulaidl.core import workflow_closure_pb2 as _workflow_closure_pb2

from nebulakit.models import common as _common
from nebulakit.models import task as _task_models
from nebulakit.models.core import workflow as _core_workflow_models


class WorkflowClosure(_common.NebulaIdlEntity):
    def __init__(self, workflow, tasks=None):
        """
        :param nebulakit.models.core.workflow.WorkflowTemplate workflow: Workflow template
        :param list[nebulakit.models.task.TaskTemplate] tasks: [Optional]
        """
        self._workflow = workflow
        self._tasks = tasks

    @property
    def workflow(self):
        """
        :rtype: nebulakit.models.core.workflow.WorkflowTemplate
        """
        return self._workflow

    @property
    def tasks(self):
        """
        :rtype: list[nebulakit.models.task.TaskTemplate]
        """
        return self._tasks

    def to_nebula_idl(self):
        """
        :rtype: nebulaidl.core.workflow_closure_pb2.WorkflowClosure
        """
        return _workflow_closure_pb2.WorkflowClosure(
            workflow=self.workflow.to_nebula_idl(),
            tasks=[t.to_nebula_idl() for t in self.tasks],
        )

    @classmethod
    def from_nebula_idl(cls, pb2_object):
        """
        :param nebulaidl.core.workflow_closure_pb2.WorkflowClosure pb2_object
        :rtype: WorkflowClosure
        """
        return cls(
            workflow=_core_workflow_models.WorkflowTemplate.from_nebula_idl(pb2_object.workflow),
            tasks=[_task_models.TaskTemplate.from_nebula_idl(t) for t in pb2_object.tasks],
        )
