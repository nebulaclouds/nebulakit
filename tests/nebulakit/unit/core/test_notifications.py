from nebulaidl.admin import common_pb2 as _common_pb2

from nebulakit.core import notification
from nebulakit.core.launch_plan import LaunchPlan
from nebulakit.core.task import task
from nebulakit.core.workflow import workflow
from nebulakit.models import common as _common_model
from nebulakit.models.core import execution as _execution_model

_workflow_execution_succeeded = _execution_model.WorkflowExecutionPhase.SUCCEEDED


def test_pager_duty_notification():
    pager_duty_notif = notification.PagerDuty(
        phases=[_workflow_execution_succeeded], recipients_email=["my-team@pagerduty.com"]
    )
    assert pager_duty_notif.to_nebula_idl() == _common_pb2.Notification(
        phases=[_workflow_execution_succeeded],
        email=None,
        pager_duty=_common_model.PagerDutyNotification(["my-team@pagerduty.com"]).to_nebula_idl(),
        slack=None,
    )


def test_slack_notification():
    slack_notif = notification.Slack(phases=[_workflow_execution_succeeded], recipients_email=["my-team@slack.com"])
    assert slack_notif.to_nebula_idl() == _common_pb2.Notification(
        phases=[_workflow_execution_succeeded],
        email=None,
        pager_duty=None,
        slack=_common_model.SlackNotification(["my-team@slack.com"]).to_nebula_idl(),
    )


def test_email_notification():
    email_notif = notification.Email(phases=[_workflow_execution_succeeded], recipients_email=["my-team@email.com"])
    assert email_notif.to_nebula_idl() == _common_pb2.Notification(
        phases=[_workflow_execution_succeeded],
        email=_common_model.EmailNotification(["my-team@email.com"]).to_nebula_idl(),
        pager_duty=None,
        slack=None,
    )


def test_with_launch_plan():
    @task
    def double(a: int) -> int:
        return a * 2

    @workflow
    def quadruple(a: int) -> int:
        b = double(a=a)
        c = double(a=b)
        return c

    lp = LaunchPlan.create(
        "notif_test",
        quadruple,
        notifications=[
            notification.Email(phases=[_workflow_execution_succeeded], recipients_email=["my-team@email.com"])
        ],
    )
    assert lp.notifications == [
        notification.Email(phases=[_workflow_execution_succeeded], recipients_email=["my-team@email.com"])
    ]
