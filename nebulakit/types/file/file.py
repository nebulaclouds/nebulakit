from __future__ import annotations

import mimetypes
import os
import pathlib
import typing
from contextlib import contextmanager
from dataclasses import dataclass, field

from dataclasses_json import config
from marshmallow import fields
from mashumaro.mixins.json import DataClassJSONMixin

from nebulakit.core.context_manager import NebulaContext, NebulaContextManager
from nebulakit.core.type_engine import TypeEngine, TypeTransformer, TypeTransformerFailedError, get_underlying_type
from nebulakit.loggers import logger
from nebulakit.models.core.types import BlobType
from nebulakit.models.literals import Blob, BlobMetadata, Literal, Scalar
from nebulakit.models.types import LiteralType
from nebulakit.types.pickle.pickle import NebulaPickleTransformer


def noop():
    ...


T = typing.TypeVar("T")


@dataclass
class NebulaFile(os.PathLike, typing.Generic[T], DataClassJSONMixin):
    path: typing.Union[str, os.PathLike] = field(default=None, metadata=config(mm_field=fields.String()))  # type: ignore
    """
    Since there is no native Python implementation of files and directories for the Nebula Blob type, (like how int
    exists for Nebula's Integer type) we need to create one so that users can express that their tasks take
    in or return a file. There is ``pathlib.Path`` of course, (which is usable in Nebulakit as a return value, though
    not a return type), but it made more sense to create a new type esp. since we can add on additional properties.

    Files (and directories) differ from the primitive types like floats and string in that Nebulakit typically uploads
    the contents of the files to the blob store connected with your Nebula installation. That is, the Python native
    literal that represents a file is typically just the path to the file on the local filesystem. However in Nebula,
    an instance of a file is represented by a :py:class:`Blob <nebulakit.models.literals.Blob>` literal,
    with the ``uri`` field set to the location in the Nebula blob store (AWS/GCS etc.). Take a look at the
    :std:ref:`data handling doc <nebula:divedeep-data-management>` for a deeper discussion.

    We decided to not support ``pathlib.Path`` as an input/output type because if you wanted the automatic
    upload/download behavior, you should just use the ``NebulaFile`` type. If you do not, then a ``str`` works just as
    well.

    The prefix for where uploads go is set by the raw output data prefix setting, which should be set at registration
    time in the launch plan. See the option listed under ``nebulactl register examples --help`` for more information.
    If not set in the launch plan, then your Nebula backend will specify a default. This default is itself configurable
    as well. Contact your Nebula platform administrators to change or ascertain the value.

    In short, if a task returns ``"/path/to/file"`` and the task's signature is set to return ``NebulaFile``, then the
    contents of ``/path/to/file`` are uploaded.

    You can also make it so that the upload does not happen. There are different types of
    task/workflow signatures. Keep in mind that in the backend, in Admin and in the blob store, there is only one type
    that represents files, the :py:class:`Blob <nebulakit.models.core.types.BlobType>` type.

    Whether the uploading happens or not, the behavior of the translation between Python native values and Nebula
    literal values depends on a few attributes:

    * The declared Python type in the signature. These can be
      * :class:`python:nebulakit.NebulaFile`
      * :class:`python:os.PathLike`
      Note that ``os.PathLike`` is only a type in Python, you can't instantiate it.
    * The type of the Python native value we're returning. These can be
      * :py:class:`nebulakit.NebulaFile`
      * :py:class:`pathlib.Path`
      * :py:class:`str`
    * Whether the value being converted is a "remote" path or not. For instance, if a task returns a value of
      "http://www.google.com" as a ``NebulaFile``, obviously it doesn't make sense for us to try to upload that to the
      Nebula blob store. So no remote paths are uploaded. Nebulakit considers a path remote if it starts with ``s3://``,
      ``gs://``, ``http(s)://``, or even ``file://``.

    **Converting from a Nebula literal value to a Python instance of NebulaFile**

    +-------------+---------------+---------------------------------------------+--------------------------------------+
    |             |               |              Expected Python type                                                  |
    +-------------+---------------+---------------------------------------------+--------------------------------------+
    | Type of Nebula IDL Literal   | NebulaFile                                   |  os.PathLike                         |
    +=============+===============+=============================================+======================================+
    | Blob        | uri matches   | NebulaFile object stores the original string |                                      |
    |             | http(s)/s3/gs | path, but points to a local file instead.   |                                      |
    |             |               |                                             |                                      |
    |             |               | * [fn] downloader: function that writes to  |                                      |
    |             |               |   path when open'ed.                        |                                      |
    |             |               | * [fn] download: will trigger               | Basically this signals Nebula should  |
    |             |               |   download                                  | stay out of the way. You still get   |
    |             |               | * path: randomly generated local path that  | a NebulaFile object (which implements |
    |             |               |   will not exist until downloaded           | the os.PathLike interface)           |
    |             |               | * remote_path: None                         |                                      |
    |             |               | * remote_source: original http/s3/gs path   | * [fn] downloader: noop function,    |
    |             |               |                                             |   even if it's http/s3/gs            |
    |             +---------------+---------------------------------------------+ * [fn] download: raises              |
    |             | uri matches   | NebulaFile object just wraps the string      |   exception                          |
    |             | /local/path   |                                             | * path: just the given path          |
    |             |               | * [fn] downloader: noop function            | * remote_path: None                  |
    |             |               | * [fn] download: raises exception           | * remote_source: None                |
    |             |               | * path: just the given path                 |                                      |
    |             |               | * remote_path: None                         |                                      |
    |             |               | * remote_source: None                       |                                      |
    +-------------+---------------+---------------------------------------------+--------------------------------------+

    **Converting from a Python value (NebulaFile, str, or pathlib.Path) to a Nebula literal**

    +-------------+---------------+---------------------------------------------+--------------------------------------+
    |             |               |                               Expected Python type                                 |
    +-------------+---------------+---------------------------------------------+--------------------------------------+
    | Type of Python value        | NebulaFile                                   |  os.PathLike                         |
    +=============+===============+=============================================+======================================+
    | str or      | path matches  | Blob object is returned with uri set to the given path. No uploading happens.      |
    | pathlib.Path| http(s)/s3/gs |                                                                                    |
    |             +---------------+---------------------------------------------+--------------------------------------+
    |             | path matches  | Contents of file are uploaded to the Nebula  | No warning is logged since only a    |
    |             | /local/path   | blob store (S3, GCS, etc.), in a bucket     | string is given (as opposed to a     |
    |             |               | determined by the raw_output_data_prefix    | NebulaFile). Blob object is returned  |
    |             |               | setting.                                    | with uri set to just the given path. |
    |             |               | Blob object is returned with uri pointing   | No uploading happens.                |
    |             |               | to the blob store location.                 |                                      |
    |             |               |                                             |                                      |
    +-------------+---------------+---------------------------------------------+--------------------------------------+
    | NebulaFile   | path matches  | Blob object is returned with uri set to the given path.                            |
    |             | http(s)/s3/gs | Nothing is uploaded.                                                               |
    |             +---------------+---------------------------------------------+--------------------------------------+
    |             | path matches  | Contents of file are uploaded to the Nebula  | Warning is logged since you're       |
    |             | /local/path   | blob store (S3, GCS, etc.), in a bucket     | passing a more complex object (a     |
    |             |               | determined by the raw_output_data_prefix    | NebulaFile) and expecting a simpler   |
    |             |               | setting. If remote_path is given, then that | interface (os.PathLike). Blob object |
    |             |               | is used instead of the random path. Blob    | is returned with uri set to just the |
    |             |               | object is returned with uri pointing to     | given path. No uploading happens.    |
    |             |               | the blob store location.                    |                                      |
    |             |               |                                             |                                      |
    +-------------+---------------+---------------------------------------------+--------------------------------------+

    Since Nebula file types have a string embedded in it as part of the type, you can add a
    format by specifying a string after the class like so. ::

        def t2() -> nebulakit_typing.NebulaFile["csv"]:
            return "/tmp/local_file.csv"
    """

    @classmethod
    def extension(cls) -> str:
        return ""

    @classmethod
    def new_remote_file(cls, name: typing.Optional[str] = None) -> NebulaFile:
        """
        Create a new NebulaFile object with a remote path.
        """
        ctx = NebulaContextManager.current_context()
        r = ctx.file_access.get_random_string()
        remote_path = ctx.file_access.join(ctx.file_access.raw_output_prefix, r)
        return cls(path=remote_path)

    def __class_getitem__(cls, item: typing.Union[str, typing.Type]) -> typing.Type[NebulaFile]:
        from . import FileExt

        if item is None:
            return cls

        item_string = FileExt.check_and_convert_to_str(item)

        item_string = item_string.strip().lstrip("~").lstrip(".")
        if item == "":
            return cls

        class _SpecificFormatClass(NebulaFile):
            # Get the type engine to see this as kind of a generic
            __origin__ = NebulaFile

            @classmethod
            def extension(cls) -> str:
                return item_string

        return _SpecificFormatClass

    def __init__(
        self,
        path: typing.Union[str, os.PathLike],
        downloader: typing.Callable = noop,
        remote_path: typing.Optional[typing.Union[os.PathLike, bool]] = None,
    ):
        """
        NebulaFile's init method.

        :param path: The source path that users are expected to call open() on.
        :param downloader: Optional function that can be passed that used to delay downloading of the actual fil
            until a user actually calls open().
        :param remote_path: If the user wants to return something and also specify where it should be uploaded to.
            Alternatively, if the user wants to specify a remote path for a file that's already in the blob store,
            the path should point to the location and remote_path should be set to False.
        """
        # Make this field public, so that the dataclass transformer can set a value for it
        # https://github.com/nebulaclouds/nebulakit/blob/bcc8541bd6227b532f8462563fe8aac902242b21/nebulakit/core/type_engine.py#L298
        self.path = path
        self._downloader = downloader
        self._downloaded = False
        self._remote_path = remote_path
        self._remote_source = None

    def __fspath__(self):
        # This is where a delayed downloading of the file will happen
        if not self._downloaded:
            self._downloader()
            self._downloaded = True
        return self.path

    def __eq__(self, other):
        if isinstance(other, NebulaFile):
            return (
                self.path == other.path
                and self._remote_path == other._remote_path
                and self.extension() == other.extension()
            )
        else:
            return self.path == other

    @property
    def downloaded(self) -> bool:
        return self._downloaded

    @property
    def remote_path(self) -> typing.Optional[os.PathLike]:
        # Find better ux for no-uploads in the future.
        return self._remote_path  # type: ignore

    @property
    def remote_source(self) -> str:
        """
        If this is an input to a task, and the original path is an ``s3`` bucket, Nebulakit downloads the
        file for the user. In case the user wants access to the original path, it will be here.
        """
        return typing.cast(str, self._remote_source)

    def download(self) -> str:
        return self.__fspath__()

    @contextmanager
    def open(
        self,
        mode: str,
        cache_type: typing.Optional[str] = None,
        cache_options: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ):
        """
        Returns a streaming File handle

        .. code-block:: python

            @task
            def copy_file(ff: NebulaFile) -> NebulaFile:
                new_file = NebulaFile.new_remote_file(ff.name)
                with ff.open("rb", cache_type="readahead", cache={}) as r:
                    with new_file.open("wb") as w:
                        w.write(r.read())
                return new_file

        Alternatively,

        .. code-block:: python

            @task
            def copy_file(ff: NebulaFile) -> NebulaFile:
                new_file = NebulaFile.new_remote_file(ff.name)
                with fsspec.open(f"readahead::{ff.remote_path}", "rb", readahead={}) as r:
                    with new_file.open("wb") as w:
                        w.write(r.read())
                return new_file


        :param mode: str Open mode like 'rb', 'rt', 'wb', ...
        :param cache_type: optional str Specify if caching is to be used. Cache protocol can be ones supported by
            fsspec https://filesystem-spec.readthedocs.io/en/latest/api.html#readbuffering,
            especially useful for large file reads
        :param cache_options: optional Dict[str, Any] Refer to fsspec caching options. This is strongly coupled to the
            cache_protocol
        """
        ctx = NebulaContextManager.current_context()
        final_path = self.path
        if self.remote_source:
            final_path = self.remote_source
        elif self.remote_path:
            final_path = self.remote_path
        fs = ctx.file_access.get_filesystem_for_path(final_path)
        f = fs.open(final_path, mode, cache_type=cache_type, cache_options=cache_options)
        yield f
        f.close()

    def __repr__(self):
        return self.path

    def __str__(self):
        return self.path


class NebulaFilePathTransformer(TypeTransformer[NebulaFile]):
    def __init__(self):
        super().__init__(name="NebulaFilePath", t=NebulaFile)

    @staticmethod
    def get_format(t: typing.Union[typing.Type[NebulaFile], os.PathLike]) -> str:
        if t is os.PathLike:
            return ""
        return typing.cast(NebulaFile, t).extension()

    def _blob_type(self, format: str) -> BlobType:
        return BlobType(format=format, dimensionality=BlobType.BlobDimensionality.SINGLE)

    def assert_type(
        self, t: typing.Union[typing.Type[NebulaFile], os.PathLike], v: typing.Union[NebulaFile, os.PathLike, str]
    ):
        if isinstance(v, os.PathLike) or isinstance(v, NebulaFile) or isinstance(v, str):
            return
        raise TypeError(
            f"No automatic conversion found from type {type(v)} to NebulaFile."
            f"Supported (os.PathLike, str, Nebulafile)"
        )

    def get_literal_type(self, t: typing.Union[typing.Type[NebulaFile], os.PathLike]) -> LiteralType:
        return LiteralType(blob=self._blob_type(format=NebulaFilePathTransformer.get_format(t)))

    def get_mime_type_from_extension(self, extension: str) -> str:
        extension_to_mime_type = {
            "hdf5": "text/plain",
            "joblib": "application/octet-stream",
            "python_pickle": "application/octet-stream",
            "ipynb": "application/json",
            "onnx": "application/json",
            "tfrecord": "application/octet-stream",
        }

        for ext, mimetype in mimetypes.types_map.items():
            extension_to_mime_type[ext.split(".")[1]] = mimetype

        return extension_to_mime_type[extension]

    def validate_file_type(
        self, python_type: typing.Type[NebulaFile], source_path: typing.Union[str, os.PathLike]
    ) -> None:
        """
        This method validates the type of the file at source_path against the expected python_type.
        It uses the magic library to determine the real type of the file. If the magic library is not installed,
        it logs a debug message and returns. If the actual file does not exist, it returns without raising an error.

        :param python_type: The expected type of the file
        :param source_path: The path to the file to validate
        :raises ValueError: If the real type of the file is not the same as the expected python_type
        """
        if NebulaFilePathTransformer.get_format(python_type) == "":
            return

        try:
            # isolate the exception to the libmagic import
            import magic

        except ImportError as e:
            logger.debug(f"Libmagic is not installed. Error message: {e}")
            return

        ctx = NebulaContext.current_context()
        if ctx.file_access.is_remote(source_path):
            # Skip validation for remote files. One of the use cases for NebulaFile is to point to remote files,
            # you might have access to a remote file (e.g., in s3) that you want to pass to a Nebula workflow.
            # Therefore, we should only validate NebulaFiles for which their path is considered local.
            return

        if NebulaFilePathTransformer.get_format(python_type):
            real_type = magic.from_file(source_path, mime=True)
            expected_type = self.get_mime_type_from_extension(NebulaFilePathTransformer.get_format(python_type))
            if real_type != expected_type:
                raise ValueError(f"Incorrect file type, expected {expected_type}, got {real_type}")

    def to_literal(
        self,
        ctx: NebulaContext,
        python_val: typing.Union[NebulaFile, os.PathLike, str],
        python_type: typing.Type[NebulaFile],
        expected: LiteralType,
    ) -> Literal:
        remote_path = None
        should_upload = True

        if python_val is None:
            raise TypeTransformerFailedError("None value cannot be converted to a file.")

        # Correctly handle `Annotated[NebulaFile, ...]` by extracting the origin type
        python_type = get_underlying_type(python_type)

        if not (python_type is os.PathLike or issubclass(python_type, NebulaFile)):
            raise ValueError(f"Incorrect type {python_type}, must be either a NebulaFile or os.PathLike")

        # information used by all cases
        meta = BlobMetadata(type=self._blob_type(format=NebulaFilePathTransformer.get_format(python_type)))

        if isinstance(python_val, NebulaFile):
            source_path = python_val.path
            self.validate_file_type(python_type, source_path)

            # If the object has a remote source, then we just convert it back. This means that if someone is just
            # going back and forth between a NebulaFile Python value and a Blob Nebula IDL value, we don't do anything.
            if python_val._remote_source is not None:
                return Literal(scalar=Scalar(blob=Blob(metadata=meta, uri=python_val._remote_source)))

            # If the user specified the remote_path to be False, that means no matter what, do not upload. Also if the
            # path given is already a remote path, say https://www.google.com, the concept of uploading to the Nebula
            # blob store doesn't make sense.
            if python_val.remote_path is False or ctx.file_access.is_remote(source_path):
                should_upload = False
            # If the type that's given is a simpler type, we also don't upload, and print a warning too.
            if python_type is os.PathLike:
                logger.warning(
                    f"Converting from a NebulaFile Python instance to a Blob Nebula object, but only a {python_type} was"
                    f" specified. Since a simpler type was specified, we'll skip uploading!"
                )
                should_upload = False

            # Set the remote destination if one was given instead of triggering a random one below
            remote_path = python_val.remote_path or None

        elif isinstance(python_val, pathlib.Path) or isinstance(python_val, str):
            source_path = str(python_val)
            if issubclass(python_type, NebulaFile):
                self.validate_file_type(python_type, source_path)
                if ctx.file_access.is_remote(source_path):
                    should_upload = False
                else:
                    if isinstance(python_val, pathlib.Path) and not python_val.is_file():
                        raise ValueError(f"Error converting pathlib.Path {python_val} because it's not a file.")

                    # If it's a string pointing to a local destination, then make sure it's a file.
                    if isinstance(python_val, str):
                        p = pathlib.Path(python_val)
                        if not p.is_file():
                            raise TypeTransformerFailedError(f"Error converting {python_val} because it's not a file.")
            # python_type must be os.PathLike - see check at beginning of function
            else:
                should_upload = False

        else:
            raise TypeTransformerFailedError(f"Expected NebulaFile or os.PathLike object, received {type(python_val)}")

        # If we're uploading something, that means that the uri should always point to the upload destination.
        if should_upload:
            if remote_path is not None:
                remote_path = ctx.file_access.put_data(source_path, remote_path, is_multipart=False)
            else:
                remote_path = ctx.file_access.put_raw_data(source_path)
            return Literal(scalar=Scalar(blob=Blob(metadata=meta, uri=remote_path)))
        # If not uploading, then we can only take the original source path as the uri.
        else:
            return Literal(scalar=Scalar(blob=Blob(metadata=meta, uri=source_path)))

    def to_python_value(
        self, ctx: NebulaContext, lv: Literal, expected_python_type: typing.Union[typing.Type[NebulaFile], os.PathLike]
    ) -> NebulaFile:
        try:
            uri = lv.scalar.blob.uri
        except AttributeError:
            raise TypeTransformerFailedError(f"Cannot convert from {lv} to {expected_python_type}")

        # In this condition, we still return a NebulaFile instance, but it's a simple one that has no downloading tricks
        # Using is instead of issubclass because NebulaFile does actually subclass it
        if expected_python_type is os.PathLike:
            return NebulaFile(uri)

        # Correctly handle `Annotated[NebulaFile, ...]` by extracting the origin type
        expected_python_type = get_underlying_type(expected_python_type)

        # The rest of the logic is only for NebulaFile types.
        if not issubclass(expected_python_type, NebulaFile):  # type: ignore
            raise TypeError(f"Neither os.PathLike nor NebulaFile specified {expected_python_type}")

        # This is a local file path, like /usr/local/my_file, don't mess with it. Certainly, downloading it doesn't
        # make any sense.
        if not ctx.file_access.is_remote(uri):
            return expected_python_type(uri)  # type: ignore

        # For the remote case, return an NebulaFile object that can download
        local_path = ctx.file_access.get_random_local_path(uri)

        def _downloader():
            return ctx.file_access.get_data(uri, local_path, is_multipart=False)

        expected_format = NebulaFilePathTransformer.get_format(expected_python_type)
        ff = NebulaFile.__class_getitem__(expected_format)(local_path, _downloader)
        ff._remote_source = uri

        return ff

    def guess_python_type(self, literal_type: LiteralType) -> typing.Type[NebulaFile[typing.Any]]:
        if (
            literal_type.blob is not None
            and literal_type.blob.dimensionality == BlobType.BlobDimensionality.SINGLE
            and literal_type.blob.format != NebulaPickleTransformer.PYTHON_PICKLE_FORMAT
        ):
            return NebulaFile.__class_getitem__(literal_type.blob.format)

        raise ValueError(f"Transformer {self} cannot reverse {literal_type}")


TypeEngine.register(NebulaFilePathTransformer(), additional_types=[os.PathLike])
