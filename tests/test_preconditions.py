from flask_storage import UploadSet
from flask_storage.upload_configuration import UploadConfiguration


def test_filenames(file_storage_cls):
    uset = UploadSet("files")
    uset._config = UploadConfiguration("/uploads")
    namepairs = (("foo.txt", True), ("boat.jpg", True), ("warez.exe", False))
    for name, result in namepairs:
        tfs = file_storage_cls(filename=name)
        assert uset.file_allowed(tfs, name) is result


def test_non_ascii_filename(file_storage_cls, tmpdir):
    uset = UploadSet("files")
    uset._config = UploadConfiguration(str(tmpdir))
    tfs = file_storage_cls(filename=u"天安门.jpg")
    res = uset.save(tfs)
    assert res == "jpg.jpg"
    res = uset.save(tfs, name="secret.")
    assert res == "secret.jpg"


def test_default_extensions():
    uset = UploadSet("files")
    uset._config = UploadConfiguration("/uploads")
    extpairs = (("txt", True), ("jpg", True), ("exe", False))
    for ext, result in extpairs:
        assert uset.extension_allowed(ext) is result
