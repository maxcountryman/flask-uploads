import os

import pytest
from flask import Flask
from flask_uploads import ALL
from flask_uploads import IMAGES
from flask_uploads import UploadSet
from flask_uploads import configure_uploads

SIMPLE_PICTURE = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x05\x00\x00\x00\x05"
    b"\x08\x02\x00\x00\x00\x02\r\xb1\xb2\x00\x00\x00\x0cIDAT\x08\xd7c`\xa0."
    b'\x00\x00\x00P\x00\x01"\x13\xe8u\x00\x00\x00\x00IEND\xaeB`\x82'
)


def test_autoserve_works_without_configuration(tmp_path):
    """this *feature* was pretty much undocumented

    It could lead to unwanted data disclosure.
    """
    static = tmp_path / "static"
    static.mkdir()
    image_directory = static / "images"
    image_directory.mkdir()
    p = image_directory / "snow.jpg"
    p.write_bytes(SIMPLE_PICTURE)

    app = Flask(__name__)
    photos = UploadSet("photos", IMAGES)
    app.config["UPLOADED_PHOTOS_DEST"] = str(image_directory)
    app.config["SECRET_KEY"] = os.urandom(24)
    configure_uploads(app, photos)

    with app.test_client() as client:
        with pytest.warns(None) as record:
            response = client.get("/_uploads/photos/snow.jpg")

    # autoserve will default to false in the upcoming 1.0.0 release
    # make sure the warning about the upcoming change is issued
    assert len(record) == 1
    assert "You are using the undocumented AUTOSERVE feature." in str(record[0].message)  # noqa: E501

    assert response.status == "200 OK"


def test_autoserve_does_not_work_for_non_existing_upload_set(tmp_path):
    """
    ie here a `files` UploadSet is defined,
    but the client tries to access `photos`

    Although the file is present,
    it cannot be accessed via the `photos` route.
    """

    static = tmp_path / "static"
    static.mkdir()
    image_directory = static / "images"
    image_directory.mkdir()
    p = image_directory / "snow.jpg"
    p.write_bytes(SIMPLE_PICTURE)

    app = Flask(__name__)
    files = UploadSet("files", ALL)
    app.config["UPLOADED_FILES_DEST"] = str(image_directory)
    app.config["UPLOADS_AUTOSERVE"] = True
    app.config["SECRET_KEY"] = os.urandom(24)
    configure_uploads(app, files)

    with app.test_client() as client:
        response = client.get("/_uploads/photos/snow.jpg")

    assert response.status == "404 NOT FOUND"


def test_autoserve_gets_deactivated_when_configuring_url_with_empty_string(
        tmp_path):
    static = tmp_path / "static"
    static.mkdir()
    image_directory = static / "images"
    image_directory.mkdir()
    p = image_directory / "snow.jpg"
    p.write_bytes(SIMPLE_PICTURE)

    app = Flask(__name__)
    photos = UploadSet("photos", IMAGES)
    app.config["UPLOADED_PHOTOS_DEST"] = str(image_directory)
    app.config["SECRET_KEY"] = os.urandom(24)

    # this deactivates autoserve
    app.config["UPLOADED_PHOTOS_URL"] = ""

    configure_uploads(app, photos)

    with app.test_client() as client:
        response = client.get("/_uploads/photos/snow.jpg")

    assert response.status == "404 NOT FOUND"


def test_autoserve_gets_deactivated_when_configuring_uploaded_url(tmp_path):
    static = tmp_path / "static"
    static.mkdir()
    image_directory = static / "images"
    image_directory.mkdir()
    p = image_directory / "snow.jpg"
    p.write_bytes(SIMPLE_PICTURE)

    app = Flask(__name__)
    photos = UploadSet("photos", IMAGES)
    app.config["UPLOADED_PHOTOS_DEST"] = str(image_directory)
    app.config["SECRET_KEY"] = os.urandom(24)

    # configuring this deactivates autoserve
    app.config["UPLOADED_PHOTOS_URL"] = "https://example.com/images"

    configure_uploads(app, photos)

    with app.test_client() as client:
        response = client.get("/_uploads/photos/snow.jpg")

    assert response.status == "404 NOT FOUND"


def test_autoserve_gets_deactivated_when_set_autoserve_to_false(tmp_path):
    static = tmp_path / "static"
    static.mkdir()
    image_directory = static / "images"
    image_directory.mkdir()
    p = image_directory / "snow.jpg"
    p.write_bytes(SIMPLE_PICTURE)

    app = Flask(__name__)
    photos = UploadSet("photos", IMAGES)
    app.config["UPLOADED_PHOTOS_DEST"] = str(image_directory)
    app.config["SECRET_KEY"] = os.urandom(24)

    # configuring this deactivates autoserve
    app.config["UPLOADS_AUTOSERVE"] = False

    configure_uploads(app, photos)

    with app.test_client() as client:
        response = client.get("/_uploads/photos/snow.jpg")

    assert response.status == "404 NOT FOUND"
