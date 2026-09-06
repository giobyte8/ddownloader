from quart import Blueprint, render_template
from ddownloader.dao import http_gallery_source_dao as src_dao
from ddownloader.services import directories as dir_svc
from ddownloader.web.auth import require_login


directories_app = Blueprint("directories", __name__)
directories_app.before_request(require_login)


@directories_app.route("/", methods=["GET"])
async def all():
    dirs = await dir_svc.all()
    return await render_template("directories/index.html", directories=dirs)
