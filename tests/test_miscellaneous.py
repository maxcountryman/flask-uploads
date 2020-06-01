from flask_storage.extensions import ALL, AllExcept
from flask_storage.utils import extension, lowercase_ext, addslash


def test_tfs(file_storage_cls):
    tfs = file_storage_cls(filename="foo.bar")
    assert tfs.filename == "foo.bar"
    assert tfs.name is None
    tfs.save("foo_bar.txt")
    assert tfs.saved == "foo_bar.txt"


def test_extension():
    assert extension("foo.txt") == "txt"
    assert extension("foo") == ""
    assert extension("archive.tar.gz") == "gz"
    assert extension("audio.m4a") == "m4a"


def test_lowercase_ext():
    assert lowercase_ext("foo.txt") == "foo.txt"
    assert lowercase_ext("FOO.TXT") == "FOO.txt"
    assert lowercase_ext("foo") == "foo"
    assert lowercase_ext("FOO") == "FOO"
    assert lowercase_ext("archive.tar.gz") == "archive.tar.gz"
    assert lowercase_ext("ARCHIVE.TAR.GZ") == "ARCHIVE.TAR.gz"
    assert lowercase_ext("audio.m4a") == "audio.m4a"
    assert lowercase_ext("AUDIO.M4A") == "AUDIO.m4a"


def test_addslash():
    assert addslash("http://localhost:4000") == "http://localhost:4000/"
    assert addslash("http://localhost/uploads") == "http://localhost/uploads/"
    assert addslash("http://localhost:4000/") == "http://localhost:4000/"
    assert addslash("http://localhost/uploads/") == "http://localhost/uploads/"


def test_custom_iterables():
    assert "txt" in ALL
    assert "exe" in ALL
    ax = AllExcept(["exe"])
    assert "txt" in ax
    assert "exe" not in ax
