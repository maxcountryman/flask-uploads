from flask_storage.upload_configuration import UploadConfiguration


def test_manual(app_manual):
    storage_config = app_manual.extensions["flask-storage"]["config"]
    assert storage_config["files"] == UploadConfiguration("/var/files", "http://localhost:6001/")
    assert storage_config["photos"] == UploadConfiguration("/mnt/photos", "http://localhost:6002/")


def test_serve(app_serve):
    storage_config = app_serve.extensions["flask-storage"]["config"]
    assert storage_config["files"] == UploadConfiguration("/var/files", None)
    assert storage_config["photos"] == UploadConfiguration("/mnt/photos", None)


def test_defaults(app_defaults):
    storage_config = app_defaults.extensions["flask-storage"]["config"]
    assert storage_config["files"] == UploadConfiguration(
        "/var/uploads/files", "http://localhost:6000/files/"
    )
    assert storage_config["photos"] == UploadConfiguration(
        "/var/uploads/photos", "http://localhost:6000/photos/"
    )


def test_default_serve(app_default_serve):
    storage_config = app_default_serve.extensions["flask-storage"]["config"]
    assert storage_config["files"] == UploadConfiguration("/var/uploads/files", None)
    assert storage_config["photos"] == UploadConfiguration("/var/uploads/photos", None)


def test_mixed_defaults(app_mixed_defaults):
    storage_config = app_mixed_defaults.extensions["flask-storage"]["config"]
    assert storage_config["files"] == UploadConfiguration(
        "/var/uploads/files", "http://localhost:6001/files/"
    )
    assert storage_config["photos"] == UploadConfiguration("/mnt/photos", "http://localhost:6002/")


def test_callable_default_dest(app_callable_default_dest):
    storage_config = app_callable_default_dest.extensions["flask-storage"]["config"]
    assert storage_config["files"] == UploadConfiguration("/custom/path/files", None)
    assert storage_config["photos"] == UploadConfiguration("/mnt/photos", "http://localhost:6002/")
