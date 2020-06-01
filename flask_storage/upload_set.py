import os
import posixpath

from flask import current_app, url_for
from werkzeug.datastructures import FileStorage

from .extensions import DEFAULTS
from .exceptions import UploadNotAllowed
from .utils import extension, lowercase_ext


class UploadSet:
    """
    This represents a single set of uploaded files. Each upload set is
    independent of the others. This can be reused across multiple application
    instances, as all configuration is stored on the application object itself
    and found with `flask.current_app`.

    :param name: The name of this upload set. It defaults to ``files``, but
                 you can pick any alphanumeric name you want. (For simplicity,
                 it's best to use a plural noun.)
    :param extensions: The extensions to allow uploading in this set. The
                       easiest way to do this is to add together the extension
                       presets (for example, ``TEXT + DOCUMENTS + IMAGES``).
                       It can be overridden by the configuration with the
                       `UPLOADED_X_ALLOW` and `UPLOADED_X_DENY` configuration
                       parameters. The default is `DEFAULTS`.
    :param default_dest: If given, this should be a callable. If you call it
                         with the app, it should return the default upload
                         destination path for that app.
    """

    def __init__(self, name="files", extensions=DEFAULTS, default_dest=None):
        if not name.isalnum():
            raise ValueError("Name must be alphanumeric (no underscores)")

        self.name = name
        self.extensions = extensions
        self._config = None
        self.default_dest = default_dest

    @property
    def config(self):
        """
        This gets the current configuration. By default, it looks up the
        current application and gets the configuration from there. But if you
        don't want to go to the full effort of setting an application, or it's
        otherwise outside of a request context, set the `_config` attribute to
        an `UploadConfiguration` instance, then set it back to `None` when
        you're done.
        """
        if self._config is not None:
            return self._config
        try:
            return current_app.extensions["flask-storage"]["config"][self.name]
        except AttributeError:
            raise RuntimeError("cannot access configuration outside request")

    def url(self, filename):
        """
        This function gets the URL a file uploaded to this set would be
        accessed at. It doesn't check whether said file exists.

        :param filename: The filename to return the URL for.
        """
        base = self.config.base_url
        if base is None:
            return url_for(
                "_uploads.uploaded_file", setname=self.name, filename=filename, _external=True,
            )
        else:
            return base + filename

    def path(self, filename, folder=None):
        """
        This returns the absolute path of a file uploaded to this set. It
        doesn't actually check whether said file exists.

        :param filename: The filename to return the path for.
        :param folder: The subfolder within the upload set previously used
                       to save to.
        """
        if folder is not None:
            target_folder = os.path.join(self.config.destination, folder)
        else:
            target_folder = self.config.destination
        return os.path.join(target_folder, filename)

    def file_allowed(self, storage, basename):
        """
        This tells whether a file is allowed. It should return `True` if the
        given `werkzeug.FileStorage` object can be saved with the given
        basename, and `False` if it can't. The default implementation just
        checks the extension, so you can override this if you want.

        :param storage: The `werkzeug.FileStorage` to check.
        :param basename: The basename it will be saved under.
        """
        return self.extension_allowed(extension(basename))

    def extension_allowed(self, ext):
        """
        This determines whether a specific extension is allowed. It is called
        by `file_allowed`, so if you override that but still want to check
        extensions, call back into this.

        :param ext: The extension to check, without the dot.
        """
        return (ext in self.config.allow) or (
            ext in self.extensions and ext not in self.config.deny
        )

    def get_basename(self, filename):
        return lowercase_ext(filename)

    def save(self, storage, folder=None, name=None):
        """
        This saves a `werkzeug.FileStorage` into this upload set. If the
        upload is not allowed, an `UploadNotAllowed` error will be raised.
        Otherwise, the file will be saved and its name (including the folder)
        will be returned.

        :param storage: The uploaded file to save.
        :param folder: The subfolder within the upload set to save to.
        :param name: The name to save the file as. If it ends with a dot, the
                     file's extension will be appended to the end. (If you
                     are using `name`, you can include the folder in the
                     `name` instead of explicitly using `folder`, i.e.
                     ``uset.save(file, name="someguy/photo_123.")``
        """
        if not isinstance(storage, FileStorage):
            raise TypeError("storage must be a werkzeug.FileStorage")

        if folder is None and name is not None and "/" in name:
            folder, name = os.path.split(name)

        basename = self.get_basename(storage.filename)

        if not self.file_allowed(storage, basename):
            raise UploadNotAllowed()

        if name:
            if name.endswith("."):
                basename = name + extension(basename)
            else:
                basename = name

        if folder:
            target_folder = os.path.join(self.config.destination, folder)
        else:
            target_folder = self.config.destination
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        if os.path.exists(os.path.join(target_folder, basename)):
            basename = self.resolve_conflict(target_folder, basename)

        target = os.path.join(target_folder, basename)
        storage.save(target)
        if folder:
            return posixpath.join(folder, basename)
        else:
            return basename

    def resolve_conflict(self, target_folder, basename):
        """
        If a file with the selected name already exists in the target folder,
        this method is called to resolve the conflict. It should return a new
        basename for the file.

        The default implementation splits the name and extension and adds a
        suffix to the name consisting of an underscore and a number, and tries
        that until it finds one that doesn't exist.

        :param target_folder: The absolute path to the target.
        :param basename: The file's original basename.
        """
        name, ext = os.path.splitext(basename)
        count = 0
        while True:
            count = count + 1
            newname = "%s_%d%s" % (name, count, ext)
            if not os.path.exists(os.path.join(target_folder, newname)):
                return newname
