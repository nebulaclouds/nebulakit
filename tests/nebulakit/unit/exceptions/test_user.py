from nebulakit.exceptions import base, user


def test_nebula_user_exception():
    try:
        raise user.NebulaUserException("bad")
    except Exception as e:
        assert str(e) == "bad"
        assert isinstance(type(e), base._NebulaCodedExceptionMetaclass)
        assert type(e).error_code == "USER:Unknown"
        assert isinstance(e, base.NebulaException)


def test_nebula_type_exception():
    try:
        raise user.NebulaTypeException("int", "float", received_value=1, additional_msg="That was a bad idea!")
    except Exception as e:
        assert str(e) == "Type error!  Received: int with value: 1, Expected: float. That was a bad idea!"
        assert isinstance(e, TypeError)
        assert type(e).error_code == "USER:TypeError"
        assert isinstance(e, user.NebulaUserException)

    try:
        raise user.NebulaTypeException(
            "int",
            ("list", "set"),
            received_value=1,
            additional_msg="That was a bad idea!",
        )
    except Exception as e:
        assert (
            str(e) == "Type error!  Received: int with value: 1, Expected one of: ('list', 'set'). That was a "
            "bad idea!"
        )
        assert isinstance(e, TypeError)
        assert type(e).error_code == "USER:TypeError"
        assert isinstance(e, user.NebulaUserException)

    try:
        raise user.NebulaTypeException("int", "float", additional_msg="That was a bad idea!")
    except Exception as e:
        assert str(e) == "Type error!  Received: int, Expected: float. That was a bad idea!"
        assert isinstance(e, TypeError)
        assert type(e).error_code == "USER:TypeError"
        assert isinstance(e, user.NebulaUserException)

    try:
        raise user.NebulaTypeException("int", ("list", "set"), additional_msg="That was a bad idea!")
    except Exception as e:
        assert str(e) == "Type error!  Received: int, Expected one of: ('list', 'set'). That was a " "bad idea!"
        assert isinstance(e, TypeError)
        assert type(e).error_code == "USER:TypeError"
        assert isinstance(e, user.NebulaUserException)


def test_nebula_value_exception():
    try:
        raise user.NebulaValueException(-1, "Expected a value > 0")
    except user.NebulaValueException as e:
        assert str(e) == "Value error!  Received: -1. Expected a value > 0"
        assert isinstance(e, ValueError)
        assert type(e).error_code == "USER:ValueError"
        assert isinstance(e, user.NebulaUserException)


def test_nebula_assert():
    try:
        raise user.NebulaAssertion("I ASSERT THAT THIS IS WRONG!")
    except user.NebulaAssertion as e:
        assert str(e) == "I ASSERT THAT THIS IS WRONG!"
        assert isinstance(e, AssertionError)
        assert type(e).error_code == "USER:AssertionError"
        assert isinstance(e, user.NebulaUserException)


def test_nebula_validation_error():
    try:
        raise user.NebulaValidationException("I validated that your stuff was wrong.")
    except user.NebulaValidationException as e:
        assert str(e) == "I validated that your stuff was wrong."
        assert isinstance(e, AssertionError)
        assert type(e).error_code == "USER:ValidationError"
        assert isinstance(e, user.NebulaUserException)
