from flask_uploads import UploadConfiguration


def test_manual(app_manual):
    set_config = app_manual.upload_set_config
    assert set_config["files"] == UploadConfiguration("/var/files", "http://localhost:6001/")
    assert set_config["photos"] == UploadConfiguration("/mnt/photos", "http://localhost:6002/")


def test_serve(app_serve):
    set_config = app_serve.upload_set_config
    assert set_config["files"] == UploadConfiguration("/var/files", None)
    assert set_config["photos"] == UploadConfiguration("/mnt/photos", None)


def test_defaults(app_defaults):
    set_config = app_defaults.upload_set_config
    assert set_config["files"] == UploadConfiguration(
        "/var/uploads/files", "http://localhost:6000/files/"
    )
    assert set_config["photos"] == UploadConfiguration(
        "/var/uploads/photos", "http://localhost:6000/photos/"
    )


def test_default_serve(app_default_serve):
    set_config = app_default_serve.upload_set_config
    assert set_config["files"] == UploadConfiguration("/var/uploads/files", None)
    assert set_config["photos"] == UploadConfiguration("/var/uploads/photos", None)


def test_mixed_defaults(app_mixed_defaults):
    set_config = app_mixed_defaults.upload_set_config
    assert set_config["files"] == UploadConfiguration(
        "/var/uploads/files", "http://localhost:6001/files/"
    )
    assert set_config["photos"] == UploadConfiguration("/mnt/photos", "http://localhost:6002/")


def test_callable_default_dest(app_callable_default_dest):
    set_config = app_callable_default_dest.upload_set_config
    assert set_config["files"] == UploadConfiguration("/custom/path/files", None)
    assert set_config["photos"] == UploadConfiguration("/mnt/photos", "http://localhost:6002/")
