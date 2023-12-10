import mock

from nebulakit import NebulaContext
from nebulakit.types.directory import NebulaDirectory
from nebulakit.types.file import NebulaFile


def test_new_file_dir():
    fd = NebulaDirectory(path="s3://my-bucket")
    assert fd.sep == "/"
    inner_dir = fd.new_dir("test")
    assert inner_dir.path == "s3://my-bucket/test"
    fd = NebulaDirectory(path="s3://my-bucket/")
    inner_dir = fd.new_dir("test")
    assert inner_dir.path == "s3://my-bucket/test"
    f = inner_dir.new_file("test")
    assert isinstance(f, NebulaFile)
    assert f.path == "s3://my-bucket/test/test"


def test_new_remote_dir():
    fd = NebulaDirectory.new_remote()
    assert NebulaContext.current_context().file_access.raw_output_prefix in fd.path


@mock.patch("nebulakit.types.directory.types.os.name", "nt")
def test_sep_nt():
    fd = NebulaDirectory(path="file://mypath")
    assert fd.sep == "\\"
    fd = NebulaDirectory(path="s3://mypath")
    assert fd.sep == "/"
