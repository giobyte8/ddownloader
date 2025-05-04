import logging
from quart import Blueprint, request
from ddownloader.models import HttpGallerySourceItem, SrcItemRemoteStatus
from ddownloader.dao import http_gl_src_item_dao as src_item_dao
from .security import api_key_hooks_required


hooks_api = Blueprint("hooks", __name__)
logger = logging.getLogger(__name__)


@hooks_api.route("/source/<uuid:src_id>/downloaded", methods=["POST"])
@api_key_hooks_required()
async def file_downloaded(src_id):
    jReq = await request.get_json()
    filename = jReq.get("filename")
    logger.debug(
        f"Running 'downloaded' hook for src: { src_id } "
        f"and filename: {filename}"
    )

    item = HttpGallerySourceItem(
        source_id=src_id,
        filename=filename,
        remote_status=SrcItemRemoteStatus.FOUND
    )
    item = await src_item_dao.upsert(item)

    return '', 201


@hooks_api.route("/source/<uuid:src_id>/skipped", methods=["POST"])
@api_key_hooks_required()
async def file_skipped(src_id):
    jReq = await request.get_json()
    filename = jReq.get("filename")
    logger.debug(
        f"Running 'skipped' hook for src: { src_id } "
        f"and filename: {filename}"
    )

    await src_item_dao.update_status_by_src_id_and_filename(
        src_id=src_id,
        filename=filename,
        status=SrcItemRemoteStatus.FOUND
    )
    return '', 201
