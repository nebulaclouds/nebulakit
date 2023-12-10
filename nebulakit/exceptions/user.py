import typing

from nebulakit.exceptions.base import NebulaException as _NebulaException
from nebulakit.exceptions.base import NebulaRecoverableException as _Recoverable


class NebulaUserException(_NebulaException):
    _ERROR_CODE = "USER:Unknown"


class NebulaTypeException(NebulaUserException, TypeError):
    _ERROR_CODE = "USER:TypeError"

    @staticmethod
    def _is_a_container(value):
        return isinstance(value, list) or isinstance(value, tuple) or isinstance(value, set)

    @classmethod
    def _create_verbose_message(cls, received_type, expected_type, received_value=None, additional_msg=None):
        if received_value is not None:
            return "Type error!  Received: {} with value: {}, Expected{}: {}. {}".format(
                received_type,
                received_value,
                " one of" if NebulaTypeException._is_a_container(expected_type) else "",
                expected_type,
                additional_msg or "",
            )
        else:
            return "Type error!  Received: {}, Expected{}: {}. {}".format(
                received_type,
                " one of" if NebulaTypeException._is_a_container(expected_type) else "",
                expected_type,
                additional_msg or "",
            )

    def __init__(self, received_type, expected_type, additional_msg=None, received_value=None):
        super(NebulaTypeException, self).__init__(
            self._create_verbose_message(
                received_type,
                expected_type,
                received_value=received_value,
                additional_msg=additional_msg,
            )
        )


class NebulaValueException(NebulaUserException, ValueError):
    _ERROR_CODE = "USER:ValueError"

    @classmethod
    def _create_verbose_message(cls, received_value, error_message):
        return "Value error!  Received: {}. {}".format(received_value, error_message)

    def __init__(self, received_value, error_message):
        super(NebulaValueException, self).__init__(self._create_verbose_message(received_value, error_message))


class NebulaAssertion(NebulaUserException, AssertionError):
    _ERROR_CODE = "USER:AssertionError"


class NebulaValidationException(NebulaAssertion):
    _ERROR_CODE = "USER:ValidationError"


class NebulaDisapprovalException(NebulaAssertion):
    _ERROR_CODE = "USER:ResultNotApproved"


class NebulaEntityAlreadyExistsException(NebulaAssertion):
    _ERROR_CODE = "USER:EntityAlreadyExists"


class NebulaEntityNotExistException(NebulaAssertion):
    _ERROR_CODE = "USER:EntityNotExist"


class NebulaTimeout(NebulaAssertion):
    _ERROR_CODE = "USER:Timeout"


class NebulaRecoverableException(NebulaUserException, _Recoverable):
    _ERROR_CODE = "USER:Recoverable"


class NebulaAuthenticationException(NebulaAssertion):
    _ERROR_CODE = "USER:AuthenticationError"


class NebulaInvalidInputException(NebulaUserException):
    _ERROR_CODE = "USER:BadInputToAPI"

    def __init__(self, request: typing.Any):
        self.request = request
        super().__init__()


class NebulaPromiseAttributeResolveException(NebulaAssertion):
    _ERROR_CODE = "USER:PromiseAttributeResolveError"
