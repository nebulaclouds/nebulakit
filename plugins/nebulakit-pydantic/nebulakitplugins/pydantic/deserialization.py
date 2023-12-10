import contextlib
from typing import Any, Callable, Dict, Generator, Iterator, List, Optional, Type, TypeVar, Union, cast

import pydantic
from nebulakitplugins.pydantic import commons, serialization

from nebulakit.core import context_manager, type_engine
from nebulakit.models import literals
from nebulakit.types import directory, file

# this field is used by pydantic to get the validator method
PYDANTIC_VALIDATOR_METHOD_NAME = pydantic.BaseModel.__get_validators__.__name__
PythonType = TypeVar("PythonType")  # target type of the deserialization


class PydanticDeserializationLiteralStore:
    """
    The purpose of this class is to provide a context manager that can be used to deserialize a basemodel from a
    literal map.

    Because pydantic validators are fixed when subclassing a BaseModel, this object is a singleton that
    serves as a namespace that can be set with the attach_to_literalmap context manager for the time that
    a basemodel is being deserialized. The validators are then accessing this namespace for the nebulaobj
    placeholders that it is trying to deserialize.
    """

    literal_store: Optional[serialization.LiteralStore] = None  # attachement point for the literal map

    def __init__(self) -> None:
        raise Exception("This class should not be instantiated")

    def __init_subclass__(cls) -> None:
        raise Exception("This class should not be subclassed")

    @classmethod
    @contextlib.contextmanager
    def attach(cls, literal_map: literals.LiteralMap) -> Generator[None, None, None]:
        """
        Read a literal map and populate the object store from it.

        This can be used as a context manager to attach to a literal map for the duration of a deserialization
        Note that this is not threadsafe, and designed to manage a single deserialization at a time.
        """
        assert not cls.is_attached(), "can only be attached to one literal map at a time."
        try:
            cls.literal_store = literal_map.literals
            yield
        finally:
            cls.literal_store = None

    @classmethod
    def contains(cls, item: commons.LiteralObjID) -> bool:
        assert cls.is_attached(), "can only check for existence of a literal when attached to a literal map"
        assert cls.literal_store is not None
        return item in cls.literal_store

    @classmethod
    def is_attached(cls) -> bool:
        return cls.literal_store is not None

    @classmethod
    def get_python_object(
        cls, identifier: commons.LiteralObjID, expected_type: Type[PythonType]
    ) -> Optional[PythonType]:
        """Deserialize a nebula literal and return the python object."""
        if not cls.is_attached():
            raise Exception("Must attach to a literal map before deserializing")
        literal = cls.literal_store[identifier]  # type: ignore
        python_object = deserialize_nebula_literal(literal, expected_type)
        return python_object


def set_validators_on_supported_nebula_types() -> None:
    """
    Set pydantic validator for the nebula types supported by this plugin.
    """
    for nebula_type in commons.PYDANTIC_SUPPORTED_NEBULA_TYPES:
        setattr(nebula_type, PYDANTIC_VALIDATOR_METHOD_NAME, add_nebula_validators_for_type(nebula_type))


def add_nebula_validators_for_type(
    nebula_obj_type: Type[type_engine.T],
) -> Callable[[Any], Iterator[Callable[[Any], type_engine.T]]]:
    """
    Add nebula deserialisation validators to a type.
    """

    previous_validators = cast(
        Iterator[Callable[[Any], type_engine.T]],
        getattr(nebula_obj_type, PYDANTIC_VALIDATOR_METHOD_NAME, lambda *_: [])(),
    )

    def validator(object_uid_maybe: Union[commons.LiteralObjID, Any]) -> Union[type_engine.T, Any]:
        """Partial of deserialize_nebula_literal with the object_type fixed"""
        if not PydanticDeserializationLiteralStore.is_attached():
            return object_uid_maybe  # this validator should only trigger when we are deserializeing
        if not isinstance(object_uid_maybe, str):
            return object_uid_maybe  # object uids are strings and we dont want to trigger on other types
        if not PydanticDeserializationLiteralStore.contains(object_uid_maybe):
            return object_uid_maybe  # final safety check to make sure that the object uid is in the literal map
        return PydanticDeserializationLiteralStore.get_python_object(object_uid_maybe, nebula_obj_type)

    def validator_generator(*args, **kwags) -> Iterator[Callable[[Any], type_engine.T]]:
        """Generator that returns validators."""
        yield validator
        yield from previous_validators
        yield from ADDITIONAL_NEBULATYPE_VALIDATORS.get(nebula_obj_type, [])

    return validator_generator


def validate_nebulafile(nebulafile: Union[str, file.NebulaFile]) -> file.NebulaFile:
    """Validate a nebulafile (i.e. deserialize)."""
    if isinstance(nebulafile, file.NebulaFile):
        return nebulafile
    if isinstance(nebulafile, str):  # when e.g. initializing from config
        return file.NebulaFile(nebulafile)
    else:
        raise ValueError(f"Invalid type for nebulafile: {type(nebulafile)}")


def validate_nebuladir(nebuladir: Union[str, directory.NebulaDirectory]) -> directory.NebulaDirectory:
    """Validate a nebuladir (i.e. deserialize)."""
    if isinstance(nebuladir, directory.NebulaDirectory):
        return nebuladir
    if isinstance(nebuladir, str):  # when e.g. initializing from config
        return directory.NebulaDirectory(nebuladir)
    else:
        raise ValueError(f"Invalid type for nebuladir: {type(nebuladir)}")


ADDITIONAL_NEBULATYPE_VALIDATORS: Dict[Type, List[Callable[[Any], Any]]] = {
    file.NebulaFile: [validate_nebulafile],
    directory.NebulaDirectory: [validate_nebuladir],
}


def deserialize_nebula_literal(
    nebulaobj_literal: literals.Literal, python_type: Type[PythonType]
) -> Optional[PythonType]:
    """Deserialize a Nebula Literal into the python object instance."""
    ctx = context_manager.NebulaContext.current_context()
    transformer = type_engine.TypeEngine.get_transformer(python_type)
    python_obj = transformer.to_python_value(ctx, nebulaobj_literal, python_type)
    return python_obj
