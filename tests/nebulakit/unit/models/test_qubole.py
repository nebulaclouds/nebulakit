from nebulakit.models import qubole


def test_hive_query():
    q = qubole.HiveQuery(query="some query", timeout_sec=10, retry_count=0)
    q2 = qubole.HiveQuery.from_nebula_idl(q.to_nebula_idl())
    assert q == q2
    assert q2.query == "some query"


def test_hive_job():
    query = qubole.HiveQuery(query="some query", timeout_sec=10, retry_count=0)
    obj = qubole.QuboleHiveJob(query=query, cluster_label="default", tags=[])
    obj2 = qubole.QuboleHiveJob.from_nebula_idl(obj.to_nebula_idl())
    assert obj == obj2
