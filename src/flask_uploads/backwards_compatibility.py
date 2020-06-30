import warnings


def patch_request_class(app, size=64 * 1024 * 1024):  # pragma: no cover
    """Attention!

    This function is deprecated and due to removal in `Flask-Reuploaded 1.0`.

    It was necessary to restrict the max upload size,
    back in the days of Flask 0.6 and earlier.

    By default, Flask will accept uploads to an arbitrary size. While Werkzeug
    switches uploads from memory to a temporary file when they hit 500 KiB,
    it's still possible for someone to overload your disk space with a
    gigantic file.

    This patches the app's request class's
    `~werkzeug.BaseRequest.max_content_length` attribute so that any upload
    larger than the given size is rejected with an HTTP error.

    .. note::

       In Flask 0.6, you can do this by setting the `MAX_CONTENT_LENGTH`
       setting, without patching the request class. To emulate this behavior,
       you can pass `None` as the size (you must pass it explicitly). That is
       the best way to call this function, as it won't break the Flask 0.6
       functionality if it exists.

    .. versionchanged:: 0.1.1

    :param app: The app to patch the request class of.
    :param size: The maximum size to accept, in bytes. The default is 64 MiB.
                 If it is `None`, the app's `MAX_CONTENT_LENGTH` configuration
                 setting will be used to patch.
    """
    warnings.warn(
        "`patch_request_class` is deprecated "
        "and due for removal in `Flask-Reuploaded 1.0. "
        "Please use `MAX_CONTENT_LENGTH` instead. "
        "For further help please see the documentation.",
        DeprecationWarning
    )
    if size is None:
        if isinstance(app.request_class.__dict__['max_content_length'],
                      property):
            return
        size = app.config.get('MAX_CONTENT_LENGTH')
    reqclass = app.request_class
    patched = type(reqclass.__name__, (reqclass,),
                   {'max_content_length': size})
    app.request_class = patched
