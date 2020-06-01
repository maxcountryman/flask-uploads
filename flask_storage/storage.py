import os

from .blueprint import bp
from .upload_configuration import UploadConfiguration
from .utils import addslash


class Storage:
    def __init__(self, *upload_sets, app=None):
        self.upload_sets = upload_sets

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self._app = app

        app.extensions = getattr(app, "extensions", {})
        ext = app.extensions.setdefault("flask-storage", {})
        ext["ext_obj"] = self
        ext["config"] = {}

        for uset in self.upload_sets:
            config = self._configure_upload_set(uset)
            ext["config"][uset.name] = config

        should_serve = any(s.base_url is None for s in ext["config"].values())
        if "_uploads" not in app.blueprints and should_serve:
            app.register_blueprint(bp)

    def _configure_upload_set(self, uset):
        cfg = self._app.config

        prefix = f"UPLOADED_{uset.name.upper()}_"
        using_defaults = False

        defaults = {
            "dest": self._app.config.get("UPLOADS_DEFAULT_DEST"),
            "url": self._app.config.get("UPLOADS_DEFAULT_URL"),
        }

        allow_extns = tuple(cfg.get(prefix + "ALLOW", ()))
        deny_extns = tuple(cfg.get(prefix + "DENY", ()))

        destination = cfg.get(prefix + "DEST")
        base_url = cfg.get(prefix + "URL")

        if destination is None:
            if uset.default_dest:
                destination = uset.default_dest(self._app)
            if destination is None:
                if defaults["dest"] is not None:
                    using_defaults = True
                    destination = os.path.join(defaults["dest"], uset.name)
                else:
                    raise RuntimeError("No destination for set %s" % uset.name)

        if base_url is None and using_defaults and defaults["url"]:
            base_url = addslash(defaults["url"]) + uset.name + "/"

        return UploadConfiguration(destination, base_url, allow_extns, deny_extns)
