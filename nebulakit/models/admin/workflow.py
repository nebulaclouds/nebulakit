import typing

from nebulaidl.admin import workflow_pb2 as _admin_workflow

from nebulakit.models import common as _common
from nebulakit.models.core import compiler as _compiler_models
from nebulakit.models.core import identifier as _identifier
from nebulakit.models.core import workflow as _core_workflow
from nebulakit.models.documentation import Documentation


class WorkflowSpec(_common.NebulaIdlEntity):
    def __init__(
        self,
        template: _core_workflow.WorkflowTemplate,
        sub_workflows: typing.List[_core_workflow.WorkflowTemplate],
        docs: typing.Optional[Documentation] = None,
    ):
        """
        This object fully encapsulates the specification of a workflow
        :param nebulakit.models.core.workflow.WorkflowTemplate template:
        :param list[nebulakit.models.core.workflow.WorkflowTemplate] sub_workflows:
        """
        self._template = template
        self._sub_workflows = sub_workflows
        self._docs = docs

    @property
    def template(self):
        """
        :rtype: nebulakit.models.core.workflow.WorkflowTemplate
        """
        return self._template

    @property
    def sub_workflows(self):
        """
        :rtype: list[nebulakit.models.core.workflow.WorkflowTemplate]
        """
        return self._sub_workflows

    @property
    def docs(self):
        """
        :rtype: Description entity for the workflow
        """
        return self._docs

    def to_nebula_idl(self):
        """
        :rtype: nebulaidl.admin.workflow_pb2.WorkflowSpec
        """
        return _admin_workflow.WorkflowSpec(
            template=self._template.to_nebula_idl(),
            sub_workflows=[s.to_nebula_idl() for s in self._sub_workflows],
            description=self._docs.to_nebula_idl() if self._docs else None,
        )

    @classmethod
    def from_nebula_idl(cls, pb2_object):
        """
        :param pb2_object: nebulaidl.admin.workflow_pb2.WorkflowSpec
        :rtype: WorkflowSpec
        """
        return cls(
            _core_workflow.WorkflowTemplate.from_nebula_idl(pb2_object.template),
            [_core_workflow.WorkflowTemplate.from_nebula_idl(s) for s in pb2_object.sub_workflows],
            Documentation.from_nebula_idl(pb2_object.description) if pb2_object.description else None,
        )


class Workflow(_common.NebulaIdlEntity):
    def __init__(self, id, closure):
        """
        :param nebulakit.models.core.identifier.Identifier id:
        :param WorkflowClosure closure:
        """
        self._id = id
        self._closure = closure

    @property
    def id(self):
        """
        :rtype: nebulakit.models.core.identifier.Identifier
        """
        return self._id

    @property
    def closure(self):
        """
        :rtype: WorkflowClosure
        """
        return self._closure

    def to_nebula_idl(self):
        """
        :rtype: nebulaidl.admin.workflow_pb2.Workflow
        """
        return _admin_workflow.Workflow(id=self.id.to_nebula_idl(), closure=self.closure.to_nebula_idl())

    @classmethod
    def from_nebula_idl(cls, pb2_object):
        """
        :param nebulaidl.admin.workflow_pb2.Workflow pb2_object:
        :return: Workflow
        """
        return cls(
            id=_identifier.Identifier.from_nebula_idl(pb2_object.id),
            closure=WorkflowClosure.from_nebula_idl(pb2_object.closure),
        )


class WorkflowClosure(_common.NebulaIdlEntity):
    def __init__(self, compiled_workflow):
        """
        :param nebulakit.models.core.compiler.CompiledWorkflowClosure compiled_workflow:
        """
        self._compiled_workflow = compiled_workflow

    @property
    def compiled_workflow(self):
        """
        :rtype: nebulakit.models.core.compiler.CompiledWorkflowClosure
        """
        return self._compiled_workflow

    def to_nebula_idl(self):
        """
        :rtype: nebulaidl.admin.workflow_pb2.WorkflowClosure
        """
        return _admin_workflow.WorkflowClosure(compiled_workflow=self.compiled_workflow.to_nebula_idl())

    @classmethod
    def from_nebula_idl(cls, p):
        """
        :param nebulaidl.admin.workflow_pb2.WorkflowClosure p:
        :rtype: WorkflowClosure
        """
        return cls(compiled_workflow=_compiler_models.CompiledWorkflowClosure.from_nebula_idl(p.compiled_workflow))
