from typing import Any, Dict


class NebulaAnnotation:
    """A core object to add arbitrary annotations to nebula types.

    This metadata is ingested as a python dictionary and will be serialized
    into fields on the nebulaidl type literals. This data is not accessible at
    runtime but rather can be retrieved from nebulaadmin for custom presentation
    of typed parameters.

    Nebulakit expects to receive a maximum of one `NebulaAnnotation` object
    within each typehint.

    For a task definition:

    .. code-block:: python

        @task
        def x(a: typing.Annotated[int, NebulaAnnotation({"foo": {"bar": 1}})]):
            return

    """

    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def data(self):
        return self._data
