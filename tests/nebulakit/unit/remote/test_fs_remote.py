import os
import pathlib
import shutil
import tempfile
from base64 import b64encode

import fsspec
import pytest

from nebulakit.configuration import Config
from nebulakit.core.data_persistence import FileAccessProvider
from nebulakit.remote.remote import NebulaRemote
from nebulakit.remote.remote_fs import NebulaFS

local = fsspec.filesystem("file")


@pytest.fixture
def source_folder():
    # Set up source directory for testing
    parent_temp = tempfile.mkdtemp()
    src_dir = os.path.join(parent_temp, "source", "")
    nested_dir = os.path.join(src_dir, "nested")
    local.mkdir(nested_dir)
    local.touch(os.path.join(src_dir, "original.txt"))
    with open(os.path.join(src_dir, "original.txt"), "w") as fh:
        fh.write("hello original")
    local.touch(os.path.join(nested_dir, "more.txt"))
    yield src_dir
    shutil.rmtree(parent_temp)


def test_basics():
    r = NebulaRemote(
        Config.for_sandbox(),
        default_project="nebulasnacks",
        default_domain="development",
        data_upload_location="nebula://dv1/",
    )
    fs = NebulaFS(remote=r)
    assert fs.protocol == "nebula"
    assert fs.sep == "/"
    assert fs.unstrip_protocol("dv/fwu11/") == "nebula://dv/fwu11/"


@pytest.fixture
def sandbox_remote():
    r = NebulaRemote(
        Config.for_sandbox(),
        default_project="nebulasnacks",
        default_domain="development",
        data_upload_location="nebula://data",
    )
    yield r


@pytest.mark.sandbox_test
def test_upl(sandbox_remote):
    encoded_md5 = b64encode(b"hi2dfsfj23333ileksa")
    xx = sandbox_remote.client.get_upload_signed_url(
        "nebulasnacks", "development", content_md5=encoded_md5, filename="parent/child/1"
    )
    print(xx.native_url)


@pytest.mark.sandbox_test
def test_remote_upload_with_fs_directly(sandbox_remote):
    fs = NebulaFS(remote=sandbox_remote)

    # Test uploading a folder, but without the /
    res = fs.put("/Users/ytong/temp/data/source", "nebula://data", recursive=True)
    # hash of the structure of local folder. if source/ changed, will need to update hash
    assert res == "s3://my-s3-bucket/nebulasnacks/development/KJA7JXRVACAG7OCR23GS5VLA4A======/source"

    # Test uploading a file
    res = fs.put(__file__, "nebula://data")
    assert res.startswith("s3://my-s3-bucket/nebulasnacks/development")
    assert res.endswith("test_fs_remote.py")


@pytest.mark.sandbox_test
def test_fs_direct_trailing_slash(sandbox_remote):
    fs = NebulaFS(remote=sandbox_remote)

    with tempfile.TemporaryDirectory() as tmpdir:
        temp_dir = pathlib.Path(tmpdir)
        file_name = temp_dir / "test.txt"
        file_name.write_text("bla bla bla")

        # Uploading folder with a / won't include the folder name
        res = fs.put(str(temp_dir), "nebula://data", recursive=True)
        assert (
            res
            == f"s3://my-s3-bucket/nebulasnacks/development/SUX2NK32ZQNO7F7DQMWYBVZQVM======/{temp_dir.name}/test.txt"
        )


@pytest.mark.sandbox_test
def test_remote_upload_with_data_persistence(sandbox_remote):
    sandbox_path = tempfile.mkdtemp()
    fp = FileAccessProvider(local_sandbox_dir=sandbox_path, raw_output_prefix="nebula://data/")

    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write("asdf")
        f.flush()
        # Test uploading a file and folder.
        res = fp.put(f.name, "nebula://data", recursive=True)
        # Unlike using the RemoteFS directly, the trailing slash is automatically added by data persistence, not sure why
        # but preserving the behavior for now.
        assert res == "s3://my-s3-bucket/nebulasnacks/development/KJA7JXRVACAG7OCR23GS5VLA4A======"


def test_common_matching():
    urls = [
        "s3://my-s3-bucket/nebulasnacks/development/ABCYZWMPACZAJ2MABGMOZ6CCPY======/source/empty.md",
        "s3://my-s3-bucket/nebulasnacks/development/ABCXKL5ZZWXY3PDLM3OONUHHME======/source/nested/more.txt",
        "s3://my-s3-bucket/nebulasnacks/development/ABCXBAPBKONMADXVW5Q3J6YBWM======/source/original.txt",
    ]

    assert NebulaFS.extract_common(urls) == "s3://my-s3-bucket/nebulasnacks/development"


def test_hashing(sandbox_remote, source_folder):
    fs = NebulaFS(remote=sandbox_remote)
    s = fs.get_hashes_and_lengths(pathlib.Path(source_folder))
    assert len(s) == 2
    lengths = set([x[1] for x in s.values()])
    assert lengths == {0, 14}
    fr = fs.get_filename_root(s)
    assert fr == "GSEYDOSFXWFB5ABZB6AHZ2HK7Y======"
