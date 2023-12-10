class _NebulaCodedExceptionMetaclass(type):
    @property
    def error_code(cls):
        return cls._ERROR_CODE


class NebulaException(Exception, metaclass=_NebulaCodedExceptionMetaclass):
    _ERROR_CODE = "UnknownNebulaException"


class NebulaRecoverableException(NebulaException):
    _ERROR_CODE = "RecoverableNebulaException"
