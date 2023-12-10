import typing
from typing import Union

import grpc

from nebulakit.exceptions.base import NebulaException
from nebulakit.exceptions.system import NebulaSystemException
from nebulakit.exceptions.user import (
    NebulaAuthenticationException,
    NebulaEntityAlreadyExistsException,
    NebulaEntityNotExistException,
    NebulaInvalidInputException,
)


class RetryExceptionWrapperInterceptor(grpc.UnaryUnaryClientInterceptor, grpc.UnaryStreamClientInterceptor):
    def __init__(self, max_retries: int = 3):
        self._max_retries = 3

    @staticmethod
    def _raise_if_exc(request: typing.Any, e: Union[grpc.Call, grpc.Future]):
        if isinstance(e, grpc.RpcError):
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                raise NebulaAuthenticationException() from e
            elif e.code() == grpc.StatusCode.ALREADY_EXISTS:
                raise NebulaEntityAlreadyExistsException() from e
            elif e.code() == grpc.StatusCode.NOT_FOUND:
                raise NebulaEntityNotExistException() from e
            elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise NebulaInvalidInputException(request) from e
        raise NebulaSystemException() from e

    def intercept_unary_unary(self, continuation, client_call_details, request):
        retries = 0
        while True:
            fut: grpc.Future = continuation(client_call_details, request)
            e = fut.exception()
            try:
                if e:
                    self._raise_if_exc(request, e)
                return fut
            except NebulaException as e:
                if retries == self._max_retries:
                    raise e
                retries = retries + 1

    def intercept_unary_stream(self, continuation, client_call_details, request):
        c: grpc.Call = continuation(client_call_details, request)
        return c
