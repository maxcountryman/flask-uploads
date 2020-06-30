"""public API of Flask-Reuploaded

isort:skip_file
"""
# This huge list of imports is kept on purpose,
# as `Flask-Uploads` provided them as public API,
# and `Flask-Reuploaded` tries to stay compatible.
from .backwards_compatibility import patch_request_class

from .exceptions import UploadNotAllowed

from .extensions import ALL
from .extensions import AllExcept
from .extensions import TEXT
from .extensions import DOCUMENTS
from .extensions import IMAGES
from .extensions import AUDIO
from .extensions import DATA
from .extensions import SCRIPTS
from .extensions import ARCHIVES
from .extensions import SOURCE
from .extensions import EXECUTABLES
from .extensions import DEFAULTS

from .flask_uploads import UploadConfiguration
from .flask_uploads import UploadSet
from .flask_uploads import addslash
from .flask_uploads import configure_uploads
from .flask_uploads import extension
from .flask_uploads import lowercase_ext
from .flask_uploads import config_for_set

from .test_helper import TestingFileStorage

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
    "UploadNotAllowed",
]
