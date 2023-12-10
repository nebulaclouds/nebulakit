import os
import pathlib
import tempfile
import typing
from unittest.mock import MagicMock, patch

import pytest
from typing_extensions import Annotated

import nebulakit.configuration
from nebulakit.configuration import Config, Image, ImageConfig
from nebulakit.core.context_manager import ExecutionState, NebulaContextManager
from nebulakit.core.data_persistence import FileAccessProvider, nebula_tmp_dir
from nebulakit.core.dynamic_workflow_task import dynamic
from nebulakit.core.hash import HashMethod
from nebulakit.core.launch_plan import LaunchPlan
from nebulakit.core.task import task
from nebulakit.core.type_engine import TypeEngine
from nebulakit.core.workflow import workflow
from nebulakit.models.core.types import BlobType
from nebulakit.models.literals import LiteralMap
from nebulakit.types.file.file import NebulaFile, NebulaFilePathTransformer


# Fixture that ensures a dummy local file
@pytest.fixture
def local_dummy_file():
    fd, path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, "w") as tmp:
            tmp.write("Hello world")
        yield path
    finally:
        os.remove(path)


@pytest.fixture
def local_dummy_txt_file():
    fd, path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w") as tmp:
            tmp.write("Hello World")
        yield path
    finally:
        os.remove(path)


def can_import(module_name) -> bool:
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def test_file_type_in_workflow_with_bad_format():
    @task
    def t1() -> NebulaFile[typing.TypeVar("txt")]:
        fname = "/tmp/nebulakit_test"
        with open(fname, "w") as fh:
            fh.write("Hello World\n")
        return fname

    @workflow
    def my_wf() -> NebulaFile[typing.TypeVar("txt")]:
        f = t1()
        return f

    res = my_wf()
    with open(res, "r") as fh:
        assert fh.read() == "Hello World\n"


def test_matching_file_types_in_workflow(local_dummy_txt_file):
    # TXT
    @task
    def t1(path: NebulaFile[typing.TypeVar("txt")]) -> NebulaFile[typing.TypeVar("txt")]:
        return path

    @workflow
    def my_wf(path: NebulaFile[typing.TypeVar("txt")]) -> NebulaFile[typing.TypeVar("txt")]:
        f = t1(path=path)
        return f

    res = my_wf(path=local_dummy_txt_file)
    with open(res, "r") as fh:
        assert fh.read() == "Hello World"


def test_file_types_with_naked_nebulafile_in_workflow(local_dummy_txt_file):
    @task
    def t1(path: NebulaFile[typing.TypeVar("txt")]) -> NebulaFile:
        return path

    @workflow
    def my_wf(path: NebulaFile[typing.TypeVar("txt")]) -> NebulaFile:
        f = t1(path=path)
        return f

    res = my_wf(path=local_dummy_txt_file)
    with open(res, "r") as fh:
        assert fh.read() == "Hello World"


@pytest.mark.skipif(not can_import("magic"), reason="Libmagic is not installed")
def test_mismatching_file_types(local_dummy_txt_file):
    @task
    def t1(path: NebulaFile[typing.TypeVar("txt")]) -> NebulaFile[typing.TypeVar("jpeg")]:
        return path

    @workflow
    def my_wf(path: NebulaFile[typing.TypeVar("txt")]) -> NebulaFile[typing.TypeVar("jpeg")]:
        f = t1(path=path)
        return f

    with pytest.raises(TypeError) as excinfo:
        my_wf(path=local_dummy_txt_file)
    assert "Incorrect file type, expected image/jpeg, got text/plain" in str(excinfo.value)


def test_get_mime_type_from_extension_success():
    transformer = TypeEngine.get_transformer(NebulaFile)
    assert transformer.get_mime_type_from_extension("html") == "text/html"
    assert transformer.get_mime_type_from_extension("jpeg") == "image/jpeg"
    assert transformer.get_mime_type_from_extension("png") == "image/png"
    assert transformer.get_mime_type_from_extension("hdf5") == "text/plain"
    assert transformer.get_mime_type_from_extension("joblib") == "application/octet-stream"
    assert transformer.get_mime_type_from_extension("pdf") == "application/pdf"
    assert transformer.get_mime_type_from_extension("python_pickle") == "application/octet-stream"
    assert transformer.get_mime_type_from_extension("ipynb") == "application/json"
    assert transformer.get_mime_type_from_extension("svg") == "image/svg+xml"
    assert transformer.get_mime_type_from_extension("csv") == "text/csv"
    assert transformer.get_mime_type_from_extension("onnx") == "application/json"
    assert transformer.get_mime_type_from_extension("tfrecord") == "application/octet-stream"
    assert transformer.get_mime_type_from_extension("txt") == "text/plain"


def test_get_mime_type_from_extension_failure():
    transformer = TypeEngine.get_transformer(NebulaFile)
    with pytest.raises(KeyError):
        transformer.get_mime_type_from_extension("unknown_extension")


@pytest.mark.skipif(not can_import("magic"), reason="Libmagic is not installed")
def test_validate_file_type_incorrect():
    transformer = TypeEngine.get_transformer(NebulaFile)
    source_path = "/tmp/nebulakit_test.png"
    source_file_mime_type = "image/png"
    user_defined_format = "jpeg"

    with patch.object(NebulaFilePathTransformer, "get_format", return_value=user_defined_format):
        with patch("magic.from_file", return_value=source_file_mime_type):
            with pytest.raises(
                ValueError, match=f"Incorrect file type, expected image/jpeg, got {source_file_mime_type}"
            ):
                transformer.validate_file_type(user_defined_format, source_path)


@pytest.mark.skipif(not can_import("magic"), reason="Libmagic is not installed")
def test_nebula_file_type_annotated_hashmethod(local_dummy_file):
    def calc_hash(ff: NebulaFile) -> str:
        return str(ff.path)

    HashedNebulaFile = Annotated[NebulaFile["jpeg"], HashMethod(calc_hash)]

    @task
    def t1(path: str) -> HashedNebulaFile:
        return HashedNebulaFile(path)

    @task
    def t2(ff: HashedNebulaFile) -> None:
        print(ff.path)

    @workflow
    def wf(path: str) -> None:
        ff = t1(path=path)
        t2(ff=ff)

    with pytest.raises(TypeError) as excinfo:
        wf(path=local_dummy_file)
    assert "Incorrect file type, expected image/jpeg, got text/plain" in str(excinfo.value)


def test_file_handling_remote_default_wf_input():
    SAMPLE_DATA = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"

    @task
    def t1(fname: os.PathLike) -> int:
        with open(fname, "r") as fh:
            x = len(fh.readlines())

        return x

    @workflow
    def my_wf(fname: os.PathLike = SAMPLE_DATA) -> int:
        length = t1(fname=fname)
        return length

    assert my_wf.python_interface.inputs_with_defaults["fname"][1] == SAMPLE_DATA
    sample_lp = LaunchPlan.create("test_launch_plan", my_wf)
    assert sample_lp.parameters.parameters["fname"].default.scalar.blob.uri == SAMPLE_DATA


def test_file_handling_local_file_gets_copied():
    @task
    def t1() -> NebulaFile:
        # Use this test file itself, since we know it exists.
        return __file__

    @workflow
    def my_wf() -> NebulaFile:
        return t1()

    random_dir = NebulaContextManager.current_context().file_access.get_random_local_directory()
    fs = FileAccessProvider(local_sandbox_dir=random_dir, raw_output_prefix=os.path.join(random_dir, "mock_remote"))
    ctx = NebulaContextManager.current_context()
    with NebulaContextManager.with_context(ctx.with_file_access(fs)):
        top_level_files = os.listdir(random_dir)
        assert len(top_level_files) == 1  # the nebulakit_local folder

        x = my_wf()

        # After running, this test file should've been copied to the mock remote location.
        mock_remote_files = os.listdir(os.path.join(random_dir, "mock_remote"))
        assert len(mock_remote_files) == 1  # the file
        # File should've been copied to the mock remote folder
        assert x.path.startswith(random_dir)


def test_file_handling_local_file_gets_force_no_copy():
    @task
    def t1() -> NebulaFile:
        # Use this test file itself, since we know it exists.
        return NebulaFile(__file__, remote_path=False)

    @workflow
    def my_wf() -> NebulaFile:
        return t1()

    random_dir = NebulaContextManager.current_context().file_access.get_random_local_directory()
    fs = FileAccessProvider(local_sandbox_dir=random_dir, raw_output_prefix=os.path.join(random_dir, "mock_remote"))
    ctx = NebulaContextManager.current_context()
    with NebulaContextManager.with_context(ctx.with_file_access(fs)):
        top_level_files = os.listdir(random_dir)
        assert len(top_level_files) == 1  # the nebulakit_local folder

        workflow_output = my_wf()

        # After running, this test file should've been copied to the mock remote location.
        assert not os.path.exists(os.path.join(random_dir, "mock_remote"))

        # Because Nebula doesn't presume to handle a uri that look like a raw path, the path that is returned is
        # the original.
        assert workflow_output.path == __file__


def test_file_handling_remote_file_handling():
    SAMPLE_DATA = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"

    @task
    def t1() -> NebulaFile:
        return SAMPLE_DATA

    @workflow
    def my_wf() -> NebulaFile:
        return t1()

    # This creates a random directory that we know is empty.
    random_dir = NebulaContextManager.current_context().file_access.get_random_local_directory()
    # Creating a new FileAccessProvider will add two folderst to the random dir
    print(f"Random {random_dir}")
    fs = FileAccessProvider(local_sandbox_dir=random_dir, raw_output_prefix=os.path.join(random_dir, "mock_remote"))
    ctx = NebulaContextManager.current_context()
    with NebulaContextManager.with_context(ctx.with_file_access(fs)):
        working_dir = os.listdir(random_dir)
        assert len(working_dir) == 1  # the local_nebulakit folder

        workflow_output = my_wf()

        # After running the mock remote dir should still be empty, since the workflow_output has not been used
        with pytest.raises(FileNotFoundError):
            os.listdir(os.path.join(random_dir, "mock_remote"))

        # While the literal returned by t1 does contain the web address as the uri, because it's a remote address,
        # nebulakit will translate it back into a NebulaFile object on the local drive (but not download it)
        assert workflow_output.path.startswith(random_dir)
        # But the remote source should still be the https address
        assert workflow_output.remote_source == SAMPLE_DATA

        # The act of running the workflow should create the engine dir, and the directory that will contain the
        # file but the file itself isn't downloaded yet.
        working_dir = os.listdir(os.path.join(random_dir, "local_nebulakit"))
        # This second layer should have two dirs, a random one generated by the new_execution_context call
        # and an empty folder, created by NebulaFile transformer's to_python_value function. This folder will have
        # something in it after we open() it.
        assert len(working_dir) == 1

        assert not os.path.exists(workflow_output.path)
        # # The act of opening it should trigger the download, since we do lazy downloading.
        with open(workflow_output, "rb"):
            ...
        # assert os.path.exists(workflow_output.path)
        #
        # # The file name is maintained on download.
        # assert str(workflow_output).endswith(os.path.split(SAMPLE_DATA)[1])


def test_file_handling_remote_file_handling_nebula_file():
    SAMPLE_DATA = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"

    @task
    def t1() -> NebulaFile:
        # Unlike the test above, this returns the remote path wrapped in a NebulaFile object
        return NebulaFile(SAMPLE_DATA)

    @workflow
    def my_wf() -> NebulaFile:
        return t1()

    # This creates a random directory that we know is empty.
    random_dir = NebulaContextManager.current_context().file_access.get_random_local_directory()
    # Creating a new FileAccessProvider will add two folderst to the random dir
    fs = FileAccessProvider(local_sandbox_dir=random_dir, raw_output_prefix=os.path.join(random_dir, "mock_remote"))
    ctx = NebulaContextManager.current_context()
    with NebulaContextManager.with_context(ctx.with_file_access(fs)):
        working_dir = os.listdir(random_dir)
        assert len(working_dir) == 1  # the local_nebulakit dir

        mock_remote_path = os.path.join(random_dir, "mock_remote")
        assert not os.path.exists(mock_remote_path)  # the persistence layer won't create the folder yet

        workflow_output = my_wf()

        # After running the mock remote dir should still be empty, since the workflow_output has not been used
        assert not os.path.exists(mock_remote_path)

        # While the literal returned by t1 does contain the web address as the uri, because it's a remote address,
        # nebulakit will translate it back into a NebulaFile object on the local drive (but not download it)
        assert workflow_output.path.startswith(f"{random_dir}{os.sep}local_nebulakit")
        # But the remote source should still be the https address
        assert workflow_output.remote_source == SAMPLE_DATA

        # The act of running the workflow should create the engine dir, and the directory that will contain the
        # file but the file itself isn't downloaded yet.
        working_dir = os.listdir(os.path.join(random_dir, "local_nebulakit"))
        assert len(working_dir) == 1  # local nebulakit and the downloaded file

        assert not os.path.exists(workflow_output.path)
        # # The act of opening it should trigger the download, since we do lazy downloading.
        with open(workflow_output, "rb"):
            ...
        # This second layer should have two dirs, a random one generated by the new_execution_context call
        # and an empty folder, created by NebulaFile transformer's to_python_value function. This folder will have
        # something in it after we open() it.
        working_dir = os.listdir(os.path.join(random_dir, "local_nebulakit"))
        assert len(working_dir) == 2  # local nebulakit and the downloaded file

        assert os.path.exists(workflow_output.path)

        # The file name is maintained on download.
        assert str(workflow_output).endswith(os.path.split(SAMPLE_DATA)[1])


def test_dont_convert_remotes():
    @task
    def t1(in1: NebulaFile):
        print(in1)

    @dynamic
    def dyn(in1: NebulaFile):
        t1(in1=in1)

    fd = NebulaFile("s3://anything")

    with NebulaContextManager.with_context(
        NebulaContextManager.current_context().with_serialization_settings(
            nebulakit.configuration.SerializationSettings(
                project="test_proj",
                domain="test_domain",
                version="abc",
                image_config=ImageConfig(Image(name="name", fqn="image", tag="name")),
                env={},
            )
        )
    ):
        ctx = NebulaContextManager.current_context()
        with NebulaContextManager.with_context(
            ctx.with_execution_state(ctx.new_execution_state().with_params(mode=ExecutionState.Mode.TASK_EXECUTION))
        ) as ctx:
            lit = TypeEngine.to_literal(
                ctx, fd, NebulaFile, BlobType("", dimensionality=BlobType.BlobDimensionality.SINGLE)
            )
            lm = LiteralMap(literals={"in1": lit})
            wf = dyn.dispatch_execute(ctx, lm)
            assert wf.nodes[0].inputs[0].binding.scalar.blob.uri == "s3://anything"

            with pytest.raises(TypeError, match="No automatic conversion found from type <class 'int'>"):
                TypeEngine.to_literal(
                    ctx, 3, NebulaFile, BlobType("", dimensionality=BlobType.BlobDimensionality.SINGLE)
                )


def test_download_caching():
    mock_downloader = MagicMock()
    f = NebulaFile("test", mock_downloader)
    assert not f.downloaded
    os.fspath(f)
    assert f.downloaded
    assert mock_downloader.call_count == 1
    for _ in range(10):
        os.fspath(f)
    assert mock_downloader.call_count == 1


def test_returning_a_pathlib_path(local_dummy_file):
    @task
    def t1() -> NebulaFile:
        return pathlib.Path(local_dummy_file)

    # TODO: Remove this - only here to trigger type engine
    @workflow
    def wf1() -> NebulaFile:
        return t1()

    wf_out = wf1()
    assert isinstance(wf_out, NebulaFile)
    with open(wf_out, "r") as fh:
        assert fh.read() == "Hello world"
    assert wf_out._downloaded

    # Remove the file, then call download again, it should not because _downloaded was already set.
    os.remove(wf_out.path)
    p = wf_out.download()
    assert not os.path.exists(wf_out.path)
    assert p == wf_out.path

    @task
    def t2() -> os.PathLike:
        return pathlib.Path(local_dummy_file)

    # TODO: Remove this
    @workflow
    def wf2() -> os.PathLike:
        return t2()

    wf_out = wf2()
    assert isinstance(wf_out, NebulaFile)
    with open(wf_out, "r") as fh:
        assert fh.read() == "Hello world"


def test_output_type_pathlike(local_dummy_file):
    @task
    def t1() -> os.PathLike:
        return NebulaFile(local_dummy_file)

    # TODO: Remove this - only here to trigger type engine
    @workflow
    def wf1() -> os.PathLike:
        return t1()

    wf_out = wf1()
    assert isinstance(wf_out, NebulaFile)
    with open(wf_out, "r") as fh:
        assert fh.read() == "Hello world"


def test_input_type_pathlike(local_dummy_file):
    @task
    def t1(a: os.PathLike):
        assert isinstance(a, NebulaFile)
        with open(a, "r") as fh:
            assert fh.read() == "Hello world"

    # TODO: Remove this - only here to trigger type engine
    @workflow
    def my_wf(a: NebulaFile):
        t1(a=a)

    my_wf(a=local_dummy_file)


def test_returning_folder_instead_of_file():
    @task
    def t1() -> NebulaFile:
        return pathlib.Path(tempfile.gettempdir())

    # TODO: Remove this - only here to trigger type engine
    @workflow
    def wf1() -> NebulaFile:
        return t1()

    with pytest.raises(TypeError):
        wf1()

    @task
    def t2() -> NebulaFile:
        return tempfile.gettempdir()

    # TODO: Remove this - only here to trigger type engine
    @workflow
    def wf2() -> NebulaFile:
        return t2()

    with pytest.raises(TypeError):
        wf2()


def test_bad_return():
    @task
    def t1() -> NebulaFile:
        return 1

    # TODO: Remove this - only here to trigger type engine
    @workflow
    def wf1() -> NebulaFile:
        return t1()

    with pytest.raises(TypeError):
        wf1()


def test_file_guess():
    transformer = TypeEngine.get_transformer(NebulaFile)
    lt = transformer.get_literal_type(NebulaFile["txt"])
    assert lt.blob.format == "txt"
    assert lt.blob.dimensionality == 0

    fft = transformer.guess_python_type(lt)
    assert issubclass(fft, NebulaFile)
    assert fft.extension() == "txt"

    lt = transformer.get_literal_type(NebulaFile)
    assert lt.blob.format == ""
    assert lt.blob.dimensionality == 0

    fft = transformer.guess_python_type(lt)
    assert issubclass(fft, NebulaFile)
    assert fft.extension() == ""


def test_nebula_file_in_dyn():
    @task
    def t1(path: str) -> NebulaFile:
        return NebulaFile(path)

    @dynamic
    def dyn(fs: NebulaFile):
        t2(ff=fs)

    @task
    def t2(ff: NebulaFile) -> os.PathLike:
        assert ff.remote_source == "s3://somewhere"
        assert nebula_tmp_dir in ff.path

        return ff.path

    @workflow
    def wf(path: str) -> os.PathLike:
        n1 = t1(path=path)
        dyn(fs=n1)
        return t2(ff=n1)

    assert nebula_tmp_dir in wf(path="s3://somewhere").path


def test_nebula_file_annotated_hashmethod(local_dummy_file):
    def calc_hash(ff: NebulaFile) -> str:
        return str(ff.path)

    HashedNebulaFile = Annotated[NebulaFile, HashMethod(calc_hash)]

    @task
    def t1(path: str) -> HashedNebulaFile:
        return HashedNebulaFile(path)

    @task
    def t2(ff: HashedNebulaFile) -> None:
        print(ff.path)

    @workflow
    def wf(path: str) -> None:
        ff = t1(path=path)
        t2(ff=ff)

    wf(path=local_dummy_file)


@pytest.mark.sandbox_test
def test_file_open_things():
    @task
    def write_this_file_to_s3() -> NebulaFile:
        ctx = NebulaContextManager.current_context()
        r = ctx.file_access.get_random_string()
        dest = ctx.file_access.join(ctx.file_access.raw_output_prefix, r)
        ctx.file_access.put(__file__, dest)
        return NebulaFile(path=dest)

    @task
    def copy_file(ff: NebulaFile) -> NebulaFile:
        new_file = NebulaFile.new_remote_file(ff.remote_path)
        with ff.open("r") as r:
            with new_file.open("w") as w:
                w.write(r.read())
        return new_file

    @task
    def print_file(ff: NebulaFile):
        with open(ff, "r") as fh:
            print(len(fh.readlines()))

    dc = Config.for_sandbox().data_config
    with tempfile.TemporaryDirectory() as new_sandbox:
        provider = FileAccessProvider(
            local_sandbox_dir=new_sandbox, raw_output_prefix="s3://my-s3-bucket/testdata/", data_config=dc
        )
        ctx = NebulaContextManager.current_context()
        local = ctx.file_access.get_filesystem("file")  # get a local file system.
        with NebulaContextManager.with_context(ctx.with_file_access(provider)):
            f = write_this_file_to_s3()
            copy_file(ff=f)
            files = local.find(new_sandbox)
            # copy_file was done via streaming so no files should have been written
            assert len(files) == 0
            print_file(ff=f)
            # print_file uses traditional download semantics so now a file should have been created
            files = local.find(new_sandbox)
            assert len(files) == 1


def test_join():
    ctx = NebulaContextManager.current_context()
    fs = ctx.file_access.get_filesystem("file")
    f = ctx.file_access.join("a", "b", "c", unstrip=False)
    assert f == fs.sep.join(["a", "b", "c"])

    fs = ctx.file_access.get_filesystem("s3")
    f = ctx.file_access.join("s3://a", "b", "c", fs=fs)
    assert f == fs.sep.join(["s3://a", "b", "c"])
