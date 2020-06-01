import os
from werkzeug.utils import secure_filename


def extension(filename):
    main, ext = os.path.splitext(filename)
    if ext.startswith("."):
        # os.path.splitext retains . separator
        ext = ext[1:]

    return ext


def lowercase_ext(filename):
    """
    This is a helper used by UploadSet.save to provide lowercase extensions for
    all processed files, to compare with configured extensions in the same
    case.

    :param filename: The filename to ensure has a lowercase extension.
    """
    ext = extension(filename)
    secured = secure_filename(filename)
    if not ext:
        return secured

    if "." not in secured:
        return secured + "." + ext.lower()
    else:
        main, ext = os.path.splitext(secured)
        return main + ext.lower()


def addslash(url):
    return url if url.endswith("/") else url + "/"
