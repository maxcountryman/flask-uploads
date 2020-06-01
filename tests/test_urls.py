from flask_uploads import UploadSet, url_for


def test_url_generated(app_serve):
    uset = UploadSet("files")
    with app_serve.test_request_context():
        url = uset.url("foo.txt")
        gen = url_for("_uploads.uploaded_file", setname="files", filename="foo.txt", _external=True)
        assert url == gen


def test_url_based(app_manual):
    uset = UploadSet("files")
    with app_manual.test_request_context():
        url = uset.url("foo.txt")
        assert url == "http://localhost:6001/foo.txt"

    assert "_uploads" not in app_manual.blueprints
