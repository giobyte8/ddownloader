from quart import Blueprint, render_template
from ddownloader.models import HttpGallerySource
from ddownloader.dao import http_gallery_source_dao as src_dao

sources_app = Blueprint("sources", __name__)

@sources_app.route("/", methods=["GET"])
async def all():
    sources = await src_dao.all()
    return await render_template("sources.html", sources=sources)
