from nebulakit.exceptions import base, system


def test_nebula_system_exception():
    try:
        raise system.NebulaSystemException("bad")
    except Exception as e:
        assert str(e) == "bad"
        assert isinstance(type(e), base._NebulaCodedExceptionMetaclass)
        assert type(e).error_code == "SYSTEM:Unknown"
        assert isinstance(e, base.NebulaException)


def test_nebula_not_implemented_exception():
    try:
        raise system.NebulaNotImplementedException("I'm lazy so I didn't implement this.")
    except Exception as e:
        assert str(e) == "I'm lazy so I didn't implement this."
        assert isinstance(e, NotImplementedError)
        assert type(e).error_code == "SYSTEM:NotImplemented"
        assert isinstance(e, system.NebulaSystemException)


def test_nebula_entrypoint_not_loadable_exception():
    try:
        raise system.NebulaEntrypointNotLoadable("fake.module")
    except Exception as e:
        assert str(e) == "Entrypoint is not loadable!  Could not load the module: 'fake.module'."
        assert type(e).error_code == "SYSTEM:UnloadableCode"
        assert isinstance(e, system.NebulaSystemException)

    try:
        raise system.NebulaEntrypointNotLoadable("fake.module", task_name="secret_task")
    except Exception as e:
        assert str(e) == "Entrypoint is not loadable!  Could not find the task: 'secret_task' in 'fake.module'."
        assert type(e).error_code == "SYSTEM:UnloadableCode"
        assert isinstance(e, system.NebulaSystemException)

    try:
        raise system.NebulaEntrypointNotLoadable("fake.module", additional_msg="Shouldn't have used a fake module!")
    except Exception as e:
        assert (
            str(e) == "Entrypoint is not loadable!  Could not load the module: 'fake.module' "
            "due to error: Shouldn't have used a fake module!"
        )
        assert type(e).error_code == "SYSTEM:UnloadableCode"
        assert isinstance(e, system.NebulaSystemException)

    try:
        raise system.NebulaEntrypointNotLoadable(
            "fake.module",
            task_name="secret_task",
            additional_msg="Shouldn't have used a fake module!",
        )
    except Exception as e:
        assert (
            str(e) == "Entrypoint is not loadable!  Could not find the task: 'secret_task' in 'fake.module' "
            "due to error: Shouldn't have used a fake module!"
        )
        assert type(e).error_code == "SYSTEM:UnloadableCode"
        assert isinstance(e, system.NebulaSystemException)


def test_nebula_system_assertion():
    try:
        raise system.NebulaSystemAssertion("I assert that the system messed up.")
    except Exception as e:
        assert str(e) == "I assert that the system messed up."
        assert type(e).error_code == "SYSTEM:AssertionError"
        assert isinstance(e, system.NebulaSystemException)
        assert isinstance(e, AssertionError)
