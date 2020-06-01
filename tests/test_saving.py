import os
from flask_uploads import UploadSet, UploadConfiguration, ALL


def test_saved(file_storage_cls, tmp_uploadset):
    tfs = file_storage_cls(filename="foo.txt")
    res = tmp_uploadset.save(tfs)
    assert res == "foo.txt"
    assert tfs.saved == os.path.join(tmp_uploadset.config.destination, "foo.txt")


def test_save_folders(file_storage_cls, tmp_uploadset):
    tfs = file_storage_cls(filename="foo.txt")
    res = tmp_uploadset.save(tfs, folder="someguy")
    assert res == "someguy/foo.txt"
    assert tfs.saved == os.path.join(tmp_uploadset.config.destination, "someguy", "foo.txt")


def test_save_named(file_storage_cls, tmp_uploadset):
    tfs = file_storage_cls(filename="foo.txt")
    res = tmp_uploadset.save(tfs, name="file_123.txt")
    assert res == "file_123.txt"
    assert tfs.saved == os.path.join(tmp_uploadset.config.destination, "file_123.txt")


def test_save_namedext(file_storage_cls, tmp_uploadset):
    tfs = file_storage_cls(filename="boat.jpg")
    res = tmp_uploadset.save(tfs, name="photo_123.")
    assert res == "photo_123.jpg"
    assert tfs.saved == os.path.join(tmp_uploadset.config.destination, "photo_123.jpg")


def test_folder_namedext(file_storage_cls, tmp_uploadset):
    tfs = file_storage_cls(filename="boat.jpg")
    res = tmp_uploadset.save(tfs, folder="someguy", name="photo_123.")
    assert res == "someguy/photo_123.jpg"
    assert tfs.saved == os.path.join(tmp_uploadset.config.destination, "someguy", "photo_123.jpg")


def test_implicit_folder(file_storage_cls, tmp_uploadset):
    tfs = file_storage_cls(filename="boat.jpg")
    res = tmp_uploadset.save(tfs, name="someguy/photo_123.")
    assert res == "someguy/photo_123.jpg"
    assert tfs.saved == os.path.join(tmp_uploadset.config.destination, "someguy", "photo_123.jpg")


def test_secured_filename(file_storage_cls, tmpdir):
    dst = str(tmpdir)
    uset = UploadSet("files", ALL)
    uset._config = UploadConfiguration(dst)
    tfs1 = file_storage_cls(filename="/etc/passwd")
    tfs2 = file_storage_cls(filename="../../myapp.wsgi")
    res1 = uset.save(tfs1)
    assert res1 == "etc_passwd"
    assert tfs1.saved == os.path.join(dst, "etc_passwd")
    res2 = uset.save(tfs2)
    assert res2 == "myapp.wsgi"
    assert tfs2.saved == os.path.join(dst, "myapp.wsgi")
