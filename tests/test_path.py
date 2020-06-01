from flask_uploads import UploadSet, UploadConfiguration


def test_path():
    uset = UploadSet("files")
    uset._config = UploadConfiguration("/uploads")

    assert uset.path("foo.txt") == "/uploads/foo.txt"
    assert uset.path("someguy/foo.txt") == "/uploads/someguy/foo.txt"
    assert uset.path("foo.txt", folder="someguy") == "/uploads/someguy/foo.txt"
    assert uset.path("foo/bar.txt", folder="someguy") == "/uploads/someguy/foo/bar.txt"
