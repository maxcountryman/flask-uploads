from flask import Blueprint, current_app, send_from_directory, abort


bp = Blueprint("_uploads", __name__, url_prefix="/_uploads")


@bp.route("/<setname>/<path:filename>")
def uploaded_file(setname, filename):
    config = current_app.upload_set_config.get(setname)
    if config is None:
        abort(404)

    return send_from_directory(config.destination, filename)
