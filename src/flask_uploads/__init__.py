"""public API of Flask-Reuploaded

isort:skip_file
"""
# This huge list of imports is kept on purpose,
# as `Flask-Uploads` provided them as public API,
# and `Flask-Reuploaded` tries to stay compatible.
from .flask_uploads import TestingFileStorage
from .flask_uploads import UploadConfiguration
from .flask_uploads import UploadSet
from .flask_uploads import addslash
from .flask_uploads import configure_uploads
from .flask_uploads import extension
from .flask_uploads import lowercase_ext
from .flask_uploads import patch_request_class
from .flask_uploads import config_for_set

from .flask_uploads import ALL
from .flask_uploads import AllExcept
from .flask_uploads import TEXT
from .flask_uploads import DOCUMENTS
from .flask_uploads import IMAGES
from .flask_uploads import AUDIO
from .flask_uploads import DATA
from .flask_uploads import SCRIPTS
from .flask_uploads import ARCHIVES
from .flask_uploads import SOURCE
from .flask_uploads import EXECUTABLES
from .flask_uploads import DEFAULTS


__all__ = [
    "TestingFileStorage",
    "UploadConfiguration",
    "UploadSet",
    "addslash",
    "configure_uploads",
    "extension",
    "lowercase_ext",
    "patch_request_class",
    "config_for_set",
    "ALL",
    "AllExcept",
    "TEXT",
    "DOCUMENTS",
    "IMAGES",
    "AUDIO",
    "DATA",
    "SCRIPTS",
    "ARCHIVES",
    "SOURCE",
    "EXECUTABLES",
    "DEFAULTS",
]
