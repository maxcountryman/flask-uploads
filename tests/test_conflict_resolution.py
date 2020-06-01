import pathlib

from flask_storage import UploadSet
from flask_storage.upload_configuration import UploadConfiguration


def test_conflict(file_storage_cls, tmp_uploadset):
    tfs = file_storage_cls(filename="foo.txt")
    foo = pathlib.Path(tmp_uploadset.config.destination) / "foo.txt"
    foo.touch()
    res = tmp_uploadset.save(tfs)
    assert res == "foo_1.txt"


def test_multi_conflict(file_storage_cls, tmp_uploadset):
    tfs = file_storage_cls(filename="foo.txt")
    foo = pathlib.Path(tmp_uploadset.config.destination) / "foo.txt"
    foo.touch()
    for n in range(1, 6):
        foo_n = pathlib.Path(tmp_uploadset.config.destination) / f"foo_{n}.txt"
        foo_n.touch()

    res = tmp_uploadset.save(tfs)
    assert res == "foo_6.txt"


def test_conflict_without_extension(file_storage_cls, tmpdir):
    # Test case for issue #7.
    dst = str(tmpdir)
    upload_set = UploadSet("files", extensions=(""))
    upload_set._config = UploadConfiguration(dst)

    tfs = file_storage_cls(filename="foo")
    foo = pathlib.Path(upload_set.config.destination) / "foo"
    foo.touch()

    res = upload_set.save(tfs)
    assert res == "foo_1"
