import pytest
from nebulaidl.admin.signal_pb2 import Signal, SignalList
from mock import MagicMock

from nebulakit.configuration import Config
from nebulakit.core.context_manager import NebulaContextManager
from nebulakit.core.type_engine import TypeEngine
from nebulakit.models.core.identifier import SignalIdentifier, WorkflowExecutionIdentifier
from nebulakit.remote.remote import NebulaRemote


@pytest.fixture
def remote():
    nebula_remote = NebulaRemote(config=Config.auto(), default_project="p1", default_domain="d1")
    nebula_remote._client_initialized = True
    return nebula_remote


def test_remote_list_signals(remote):
    ctx = NebulaContextManager.current_context()
    wfeid = WorkflowExecutionIdentifier("p", "d", "execid")
    signal_id = SignalIdentifier(signal_id="sigid", execution_id=wfeid).to_nebula_idl()
    lt = TypeEngine.to_literal_type(int)
    signal = Signal(
        id=signal_id,
        type=lt.to_nebula_idl(),
        value=TypeEngine.to_literal(ctx, 3, int, lt).to_nebula_idl(),
    )

    mock_client = MagicMock()
    mock_client.list_signals.return_value = SignalList(signals=[signal], token="")

    remote._client = mock_client
    res = remote.list_signals("execid", "p", "d", limit=10)
    assert len(res) == 1


def test_remote_set_signal(remote):
    mock_client = MagicMock()

    def checker(request):
        assert request.id.signal_id == "sigid"
        assert request.value.scalar.primitive.integer == 3

    mock_client.set_signal.side_effect = checker

    remote._client = mock_client
    remote.set_signal("sigid", "execid", 3)
