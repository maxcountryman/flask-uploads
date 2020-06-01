import os
from unittest import mock

import pytest
from flask import Flask
from flask_storage import UploadSet, UploadConfiguration, configure_uploads
from werkzeug.datastructures import FileStorage


@pytest.fixture(scope="session")
def app():
    app = Flask("test")
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture
def app_defaults(app):
    app.config.update(
        {"UPLOADS_DEFAULT_DEST": "/var/uploads", "UPLOADS_DEFAULT_URL": "http://localhost:6000/"}
    )

    files, photos = UploadSet("files"), UploadSet("photos")
    configure_uploads(app, (files, photos,))

    yield app

    del app.config["UPLOADS_DEFAULT_DEST"]
    del app.config["UPLOADS_DEFAULT_URL"]


@pytest.fixture
def app_default_serve(app):
    app.config.update({"UPLOADS_DEFAULT_DEST": "/var/uploads"})

    files, photos = UploadSet("files"), UploadSet("photos")
    configure_uploads(app, (files, photos,))

    yield app

    del app.config["UPLOADS_DEFAULT_DEST"]
    del app.blueprints["_uploads"]


@pytest.fixture
def app_mixed_defaults(app):
    app.config.update(
        {
            "UPLOADS_DEFAULT_DEST": "/var/uploads",
            "UPLOADS_DEFAULT_URL": "http://localhost:6001/",
            "UPLOADED_PHOTOS_DEST": "/mnt/photos",
            "UPLOADED_PHOTOS_URL": "http://localhost:6002/",
        }
    )

    files, photos = UploadSet("files"), UploadSet("photos")
    configure_uploads(app, (files, photos,))

    yield app

    del app.config["UPLOADS_DEFAULT_DEST"]
    del app.config["UPLOADS_DEFAULT_URL"]
    del app.config["UPLOADED_PHOTOS_DEST"]
    del app.config["UPLOADED_PHOTOS_URL"]


@pytest.fixture
def app_callable_default_dest(app):
    app.config.update(
        {
            "CUSTOM": "/custom/path",
            "UPLOADED_PHOTOS_DEST": "/mnt/photos",
            "UPLOADED_PHOTOS_URL": "http://localhost:6002/",
        }
    )

    files = UploadSet("files", default_dest=lambda app: os.path.join(app.config["CUSTOM"], "files"))
    photos = UploadSet("photos")
    configure_uploads(app, (files, photos,))

    yield app

    del app.config["CUSTOM"]
    del app.config["UPLOADED_PHOTOS_DEST"]
    del app.config["UPLOADED_PHOTOS_URL"]
    del app.blueprints["_uploads"]


@pytest.fixture
def app_manual(app):
    app.config.update(
        {
            "UPLOADED_FILES_DEST": "/var/files",
            "UPLOADED_FILES_URL": "http://localhost:6001/",
            "UPLOADED_PHOTOS_DEST": "/mnt/photos",
            "UPLOADED_PHOTOS_URL": "http://localhost:6002/",
        }
    )

    files, photos = UploadSet("files"), UploadSet("photos")
    configure_uploads(app, (files, photos,))

    yield app

    del app.config["UPLOADED_FILES_DEST"]
    del app.config["UPLOADED_FILES_URL"]
    del app.config["UPLOADED_PHOTOS_DEST"]
    del app.config["UPLOADED_PHOTOS_URL"]


@pytest.fixture
def app_serve(app):
    app.config.update({"UPLOADED_FILES_DEST": "/var/files", "UPLOADED_PHOTOS_DEST": "/mnt/photos"})

    files, photos = UploadSet("files"), UploadSet("photos")
    configure_uploads(app, (files, photos,))

    yield app

    del app.config["UPLOADED_FILES_DEST"]
    del app.config["UPLOADED_PHOTOS_DEST"]
    del app.blueprints["_uploads"]


@pytest.fixture
def file_storage_cls():
    def save_mock(dst, buffer_size=16384):
        FileStorage.saved = dst if isinstance(dst, str) else dst.name

    with mock.patch.object(FileStorage, "save", side_effect=save_mock):
        yield FileStorage


@pytest.fixture
def tmp_uploadset(tmpdir):
    dst = str(tmpdir)
    upload_set = UploadSet("files")
    upload_set._config = UploadConfiguration(dst)

    return upload_set
