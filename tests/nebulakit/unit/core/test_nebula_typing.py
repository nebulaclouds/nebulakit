from nebulakit.types.file.file import NebulaFile


def test_filepath_equality():
    a = NebulaFile("/tmp")
    b = NebulaFile("/tmp")
    assert str(b) == "/tmp"
    assert a == b

    a = NebulaFile("/tmp")
    b = NebulaFile["pdf"]("/tmp")
    assert a != b

    a = NebulaFile("/tmp")
    b = NebulaFile("/tmp/c")
    assert a != b

    x = "jpg"
    y = ".jpg"
    a = NebulaFile[x]("/tmp")
    b = NebulaFile[y]("/tmp")
    assert a == b


def test_fdff():
    a = NebulaFile["txt"]("/tmp")
    print(a)
    b = NebulaFile["txt"]("/tmp")
    assert a == b
