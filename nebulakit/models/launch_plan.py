import typing

from nebulaidl.admin import launch_plan_pb2 as _launch_plan

from nebulakit.models import common as _common
from nebulakit.models import interface as _interface
from nebulakit.models import literals as _literals
from nebulakit.models import schedule as _schedule
from nebulakit.models import security
from nebulakit.models.core import identifier as _identifier


class LaunchPlanMetadata(_common.NebulaIdlEntity):
    def __init__(self, schedule, notifications):
        """

        :param nebulakit.models.schedule.Schedule schedule: Schedule to execute the Launch Plan
        :param list[nebulakit.models.common.Notification] notifications: List of notifications based on
            execution status transitions
        """
        self._schedule = schedule
        self._notifications = notifications

    @property
    def schedule(self):
        """
        Schedule to execute the Launch Plan
        :rtype: nebulakit.models.schedule.Schedule
        """
        return self._schedule

    @property
    def notifications(self):
        """
        List of notifications based on Execution status transitions
        :rtype: list[nebulakit.models.common.Notification]
        """
        return self._notifications

    def to_nebula_idl(self):
        """
        List of notifications based on Execution status transitions
        :rtype: nebulaidl.admin.launch_plan_pb2.LaunchPlanMetadata
        """
        return _launch_plan.LaunchPlanMetadata(
            schedule=self.schedule.to_nebula_idl() if self.schedule is not None else None,
            notifications=[n.to_nebula_idl() for n in self.notifications],
        )

    @classmethod
    def from_nebula_idl(cls, pb2_object):
        """
        :param nebulaidl.admin.launch_plan_pb2.LaunchPlanMetadata pb2_object:
        :rtype: LaunchPlanMetadata
        """
        return cls(
            schedule=_schedule.Schedule.from_nebula_idl(pb2_object.schedule)
            if pb2_object.HasField("schedule")
            else None,
            notifications=[_common.Notification.from_nebula_idl(n) for n in pb2_object.notifications],
        )


class Auth(_common.NebulaIdlEntity):
    def __init__(self, assumable_iam_role=None, kubernetes_service_account=None):
        """
        DEPRECATED. Do not use. Use nebulakit.models.common.AuthRole instead
        At most one of assumable_iam_role or kubernetes_service_account can be set.
        :param Text assumable_iam_role: IAM identity with set permissions policies.
        :param Text kubernetes_service_account: Provides an identity for workflow execution resources. Nebula deployment
            administrators are responsible for handling permissions as they relate to the service account.
        """
        self._assumable_iam_role = assumable_iam_role
        self._kubernetes_service_account = kubernetes_service_account

    @property
    def assumable_iam_role(self):
        """
        The IAM role to execute the workflow with
        :rtype: Text
        """
        return self._assumable_iam_role

    @property
    def kubernetes_service_account(self):
        """
        The kubernetes service account to execute the workflow with
        :rtype: Text
        """
        return self._kubernetes_service_account

    def to_nebula_idl(self):
        """
        :rtype: nebulaidl.admin.launch_plan_pb2.Auth
        """
        return _launch_plan.Auth(
            assumable_iam_role=self.assumable_iam_role if self.assumable_iam_role else None,
            kubernetes_service_account=self.kubernetes_service_account if self.kubernetes_service_account else None,
        )

    @classmethod
    def from_nebula_idl(cls, pb2_object):
        """
        :param nebulaidl.admin.launch_plan_pb2.Auth pb2_object:
        :rtype: Auth
        """
        return cls(
            assumable_iam_role=pb2_object.assumable_iam_role,
            kubernetes_service_account=pb2_object.kubernetes_service_account,
        )


class LaunchPlanSpec(_common.NebulaIdlEntity):
    def __init__(
        self,
        workflow_id,
        entity_metadata,
        default_inputs,
        fixed_inputs,
        labels: _common.Labels,
        annotations: _common.Annotations,
        auth_role: _common.AuthRole,
        raw_output_data_config: _common.RawOutputDataConfig,
        max_parallelism: typing.Optional[int] = None,
        security_context: typing.Optional[security.SecurityContext] = None,
    ):
        """
        The spec for a Launch Plan.

        :param nebulakit.models.core.identifier.Identifier workflow_id: Unique identifier for the workflow in question
        :param LaunchPlanMetadata entity_metadata: Metadata
        :param nebulakit.models.interface.ParameterMap default_inputs: Input values to be passed for the execution
        :param nebulakit.models.literals.LiteralMap fixed_inputs: Fixed, non-overridable inputs for the Launch Plan
        :param nebulakit.models.common.Labels:
            Any custom kubernetes labels to apply to workflows executed by this launch plan.
        :param nebulakit.models.common.Annotations annotations:
            Any custom kubernetes annotations to apply to workflows executed by this launch plan.
        :param nebulakit.models.common.AuthRole auth_role: The auth method with which to execute the workflow.
        :param nebulakit.models.common.RawOutputDataConfig raw_output_data_config: Value for where to store offloaded
            data like Blobs and Schemas.
        :param max_parallelism int: Controls the maximum number of tasknodes that can be run in parallel for the entire
            workflow. This is useful to achieve fairness. Note: MapTasks are regarded as one unit, and
            parallelism/concurrency of MapTasks is independent from this.
        :param security_context: This can be used to add security information to a LaunchPlan, which will be used by
                                 every execution
        """
        self._workflow_id = workflow_id
        self._entity_metadata = entity_metadata
        self._default_inputs = default_inputs
        self._fixed_inputs = fixed_inputs
        self._labels = labels
        self._annotations = annotations
        self._auth_role = auth_role
        self._raw_output_data_config = raw_output_data_config
        self._max_parallelism = max_parallelism
        self._security_context = security_context

    @property
    def workflow_id(self):
        """
        Unique identifier for the workflow in question
        :rtype: nebulakit.models.core.identifier.Identifier
        """
        return self._workflow_id

    @property
    def entity_metadata(self):
        """
        :rtype: LaunchPlanMetadata
        """
        return self._entity_metadata

    @property
    def default_inputs(self):
        """
        Input values to be passed for the execution
        :rtype: nebulakit.models.interface.ParameterMap
        """
        return self._default_inputs

    @property
    def fixed_inputs(self):
        """
        Fixed, non-overridable inputs for the Launch Plan
        :rtype: nebulakit.models.literals.LiteralMap
        """
        return self._fixed_inputs

    @property
    def labels(self) -> _common.Labels:
        """
        The labels to execute the workflow with
        :rtype: nebulakit.models.common.Labels
        """
        return self._labels

    @property
    def annotations(self) -> _common.Annotations:
        """
        The annotations to execute the workflow with
        :rtype: nebulakit.models.common.Annotations
        """
        return self._annotations

    @property
    def auth_role(self):
        """
        The authorization method with which to execute the workflow.
        :rtype: nebulakit.models.common.AuthRole
        """
        return self._auth_role

    @property
    def raw_output_data_config(self):
        """
        Where to store offloaded data like Blobs and Schemas
        :rtype: nebulakit.models.common.RawOutputDataConfig
        """
        return self._raw_output_data_config

    @property
    def max_parallelism(self) -> typing.Optional[int]:
        return self._max_parallelism

    @property
    def security_context(self) -> typing.Optional[security.SecurityContext]:
        return self._security_context

    def to_nebula_idl(self):
        """
        :rtype: nebulaidl.admin.launch_plan_pb2.LaunchPlanSpec
        """
        return _launch_plan.LaunchPlanSpec(
            workflow_id=self.workflow_id.to_nebula_idl(),
            entity_metadata=self.entity_metadata.to_nebula_idl(),
            default_inputs=self.default_inputs.to_nebula_idl(),
            fixed_inputs=self.fixed_inputs.to_nebula_idl(),
            labels=self.labels.to_nebula_idl(),
            annotations=self.annotations.to_nebula_idl(),
            auth_role=self.auth_role.to_nebula_idl() if self.auth_role else None,
            raw_output_data_config=self.raw_output_data_config.to_nebula_idl(),
            max_parallelism=self.max_parallelism,
            security_context=self.security_context.to_nebula_idl() if self.security_context else None,
        )

    @classmethod
    def from_nebula_idl(cls, pb2):
        """
        :param nebulaidl.admin.launch_plan_pb2.LaunchPlanSpec pb2:
        :rtype: LaunchPlanSpec
        """
        auth_role = None
        # First check the newer field, auth_role.
        if pb2.auth_role is not None and (pb2.auth_role.assumable_iam_role or pb2.auth_role.kubernetes_service_account):
            auth_role = _common.AuthRole.from_nebula_idl(pb2.auth_role)
        # Fallback to the deprecated field.
        elif pb2.auth is not None:
            if pb2.auth.assumable_iam_role:
                auth_role = _common.AuthRole(assumable_iam_role=pb2.auth.assumable_iam_role)
            else:
                auth_role = _common.AuthRole(assumable_iam_role=pb2.auth.kubernetes_service_account)

        return cls(
            workflow_id=_identifier.Identifier.from_nebula_idl(pb2.workflow_id),
            entity_metadata=LaunchPlanMetadata.from_nebula_idl(pb2.entity_metadata),
            default_inputs=_interface.ParameterMap.from_nebula_idl(pb2.default_inputs),
            fixed_inputs=_literals.LiteralMap.from_nebula_idl(pb2.fixed_inputs),
            labels=_common.Labels.from_nebula_idl(pb2.labels),
            annotations=_common.Annotations.from_nebula_idl(pb2.annotations),
            auth_role=auth_role,
            raw_output_data_config=_common.RawOutputDataConfig.from_nebula_idl(pb2.raw_output_data_config),
            max_parallelism=pb2.max_parallelism,
            security_context=security.SecurityContext.from_nebula_idl(pb2.security_context)
            if pb2.security_context
            else None,
        )


class LaunchPlanState(object):
    INACTIVE = _launch_plan.INACTIVE
    ACTIVE = _launch_plan.ACTIVE

    @classmethod
    def enum_to_string(cls, val):
        """
        :param int val:
        :rtype: Text
        """
        if val == cls.INACTIVE:
            return "INACTIVE"
        elif val == cls.ACTIVE:
            return "ACTIVE"
        else:
            return "<UNKNOWN>"


class LaunchPlanClosure(_common.NebulaIdlEntity):
    def __init__(self, state, expected_inputs, expected_outputs):
        """
        :param LaunchPlanState state: Indicate the Launch plan phase
        :param nebulakit.models.interface.ParameterMap expected_inputs: Indicates the set of inputs to execute
            the Launch plan
        :param nebulakit.models.interface.VariableMap expected_outputs: Indicates the set of outputs from the Launch plan
        """
        self._state = state
        self._expected_inputs = expected_inputs
        self._expected_outputs = expected_outputs

    @property
    def state(self):
        """
        :rtype: LaunchPlanState
        """
        return self._state

    @property
    def expected_inputs(self):
        """
        :rtype: nebulakit.models.interface.ParameterMap
        """
        return self._expected_inputs

    @property
    def expected_outputs(self):
        """
        :rtype: nebulakit.models.interface.VariableMap
        """
        return self._expected_outputs

    def to_nebula_idl(self):
        """
        :rtype: nebulaidl.admin.launch_plan_pb2.LaunchPlanClosure
        """
        return _launch_plan.LaunchPlanClosure(
            state=self.state,
            expected_inputs=self.expected_inputs.to_nebula_idl(),
            expected_outputs=self.expected_outputs.to_nebula_idl(),
        )

    @classmethod
    def from_nebula_idl(cls, pb2_object):
        """
        :param nebulaidl.admin.launch_plan_pb2.LaunchPlanClosure pb2_object:
        :rtype: LaunchPlanClosure
        """
        return cls(
            pb2_object.state,
            _interface.ParameterMap.from_nebula_idl(pb2_object.expected_inputs),
            _interface.VariableMap.from_nebula_idl(pb2_object.expected_outputs),
        )


class LaunchPlan(_common.NebulaIdlEntity):
    def __init__(self, id, spec, closure):
        """
        :param nebulakit.models.core.identifier.Identifier id:
        :param LaunchPlanSpec spec:
        :param LaunchPlanClosure closure:
        """
        self._id = id
        self._spec = spec
        self._closure = closure

    @property
    def id(self):
        """
        :rtype: nebulakit.models.core.identifier.Identifier
        """
        return self._id

    @property
    def spec(self):
        """
        :rtype: LaunchPlanSpec
        """
        return self._spec

    @property
    def closure(self):
        """
        :rtype: LaunchPlanClosure
        """
        return self._closure

    def to_nebula_idl(self):
        """
        :rtype: nebulaidl.admin.launch_plan_pb2.LaunchPlan
        """
        identifier = (
            self.id
            if self.id is not None
            else _identifier.Identifier(_identifier.ResourceType.LAUNCH_PLAN, None, None, None, None)
        )
        return _launch_plan.LaunchPlan(
            id=identifier.to_nebula_idl(),
            spec=self.spec.to_nebula_idl(),
            closure=self.closure.to_nebula_idl(),
        )

    @classmethod
    def from_nebula_idl(cls, pb2_object):
        """
        :param nebulaidl.admin.launch_plan_pb2.LaunchPlan pb2_object:
        :rtype: LaunchPlan
        """
        return cls(
            id=_identifier.Identifier.from_nebula_idl(pb2_object.id),
            spec=LaunchPlanSpec.from_nebula_idl(pb2_object.spec),
            closure=LaunchPlanClosure.from_nebula_idl(pb2_object.closure),
        )
