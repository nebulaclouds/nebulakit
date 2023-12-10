from nebulakit.exceptions import base


def test_nebula_exception():
    try:
        raise base.NebulaException("bad")
    except Exception as e:
        assert str(e) == "bad"
        assert isinstance(type(e), base._NebulaCodedExceptionMetaclass)
        assert type(e).error_code == "UnknownNebulaException"
