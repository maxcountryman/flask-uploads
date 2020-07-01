# -*- coding: utf-8 -*-
"""
flaskext.uploads
================
This module provides upload support for Flask. The basic pattern is to set up
an `UploadSet` object and upload your files to it.

:copyright: 2010 Matthew "LeafStorm" Frazier
:license:   MIT/X11, see LICENSE for details
"""

import os.path
import posixpath

from flask import Blueprint
from flask import abort
from flask import current_app
from flask import send_from_directory
from flask import url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .exceptions import UploadNotAllowed
from .extensions import DEFAULTS
from .extensions import extension
from .extensions import lowercase_ext


def addslash(url):
    if url.endswith('/'):
        return url
    return url + '/'


def config_for_set(uset, app, defaults=None):
    """
    This is a helper function for `configure_uploads` that extracts the
    configuration for a single set.

    :param uset: The upload set.
    :param app: The app to load the configuration from.
    :param defaults: A dict with keys `url` and `dest` from the
                     `UPLOADS_DEFAULT_DEST` and `DEFAULT_UPLOADS_URL`
                     settings.
    """
    config = app.config
    prefix = 'UPLOADED_%s_' % uset.name.upper()
    using_defaults = False
    if defaults is None:
        defaults = dict(dest=None, url=None)

    allow_extensions = tuple(config.get(prefix + 'ALLOW', ()))
    deny_extensions = tuple(config.get(prefix + 'DENY', ()))
    destination = config.get(prefix + 'DEST')
    base_url = config.get(prefix + 'URL')

    if destination is None:
        # the upload set's destination wasn't given
        if uset.default_dest:
            # use the "default_dest" callable
            destination = uset.default_dest(app)
        if destination is None:  # still
            # use the default dest from the config
            if defaults['dest'] is not None:
                using_defaults = True
                destination = os.path.join(defaults['dest'], uset.name)
            else:
                raise RuntimeError("no destination for set %s" % uset.name)

    if base_url is None and using_defaults and defaults['url']:
        base_url = addslash(defaults['url']) + uset.name + '/'

    return UploadConfiguration(
        destination, base_url, allow_extensions, deny_extensions)


def configure_uploads(app, upload_sets):
    """
    Call this after the app has been configured. It will go through all the
    upload sets, get their configuration, and store the configuration on the
    app. It will also register the uploads module if it hasn't been set. This
    can be called multiple times with different upload sets.

    .. versionchanged:: 0.1.3
       The uploads module/blueprint will only be registered if it is needed
       to serve the upload sets.

    :param app: The `~flask.Flask` instance to get the configuration from.
    :param upload_sets: The `UploadSet` instances to configure.
    """
    if isinstance(upload_sets, UploadSet):
        upload_sets = (upload_sets,)

    if not hasattr(app, 'upload_set_config'):
        app.upload_set_config = {}
    set_config = app.upload_set_config
    defaults = dict(dest=app.config.get('UPLOADS_DEFAULT_DEST'),
                    url=app.config.get('UPLOADS_DEFAULT_URL'))

    for uset in upload_sets:
        config = config_for_set(uset, app, defaults)
        set_config[uset.name] = config

    should_serve = any(s.base_url is None for s in set_config.values())
    if '_uploads' not in app.blueprints and should_serve:
        app.register_blueprint(uploads_mod)


class UploadConfiguration(object):
    """
    This holds the configuration for a single `UploadSet`. The constructor's
    arguments are also the attributes.

    :param destination: The directory to save files to.
    :param base_url: The URL (ending with a /) that files can be downloaded
                     from. If this is `None`, Flask-Reuploaded will serve the
                     files itself.
    :param allow: A list of extensions to allow, even if they're not in the
                  `UploadSet` extensions list.
    :param deny: A list of extensions to deny, even if they are in the
                 `UploadSet` extensions list.
    """
    def __init__(self, destination, base_url=None, allow=(), deny=()):
        self.destination = destination
        self.base_url = base_url
        self.allow = allow
        self.deny = deny

    @property
    def tuple(self):
        return (self.destination, self.base_url, self.allow, self.deny)

    def __eq__(self, other):
        return self.tuple == other.tuple


class UploadSet(object):
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
    def __init__(self, name='files', extensions=DEFAULTS, default_dest=None):
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
            return current_app.upload_set_config[self.name]
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
            return url_for('_uploads.uploaded_file', setname=self.name,
                           filename=filename, _external=True)
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
        """This tells whether a file is allowed.

        It should return `True` if the given
        `werkzeug.datastructures.FileStorage` object can be saved with
        the given basename, and `False` if it can't.

        The default implementation just checks the extension,
        so you can override this if you want.

        :param storage: The `werkzeug.datastructures.FileStorage` to check.
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
        return ((ext in self.config.allow) or
                (ext in self.extensions and ext not in self.config.deny))

    def get_basename(self, filename):
        return lowercase_ext(secure_filename(filename))

    def save(self, storage, folder=None, name=None):
        """This saves the `storage` into this upload set.

        A `storage` is a `werkzeug.datastructures.FileStorage`.

        If the upload is not allowed,
        an `UploadNotAllowed` error will be raised.

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
            if name.endswith('.'):
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
            newname = '%s_%d%s' % (name, count, ext)
            if not os.path.exists(os.path.join(target_folder, newname)):
                return newname


uploads_mod = Blueprint('_uploads', __name__, url_prefix='/_uploads')


@uploads_mod.route('/<setname>/<path:filename>')
def uploaded_file(setname, filename):
    config = current_app.upload_set_config.get(setname)
    if config is None:
        abort(404)
    return send_from_directory(config.destination, filename)
