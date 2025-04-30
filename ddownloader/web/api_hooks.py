import logging
from quart import Blueprint, request


hooks_api = Blueprint("hooks", __name__)
logger = logging.getLogger(__name__)

# TODO: Require api key
@hooks_api.route("/source/<uuid:src_id>/downloaded", methods=["POST"])
async def file_downloaded(src_id):
    jReq = await request.get_json()
    filename = jReq.get("filename")

    logger.debug(
        f"Running 'downloaded' hook for src: { src_id } "
        f"and filename: {filename}"
    )

    return '', 201


@hooks_api.route("/source/<uuid:src_id>/skipped", methods=["POST"])
async def file_skipped(src_id):
    jReq = await request.get_json()
    filename = jReq.get("filename")

    logger.debug(
        f"Running 'skipped' hook for src: { src_id } "
        f"and filename: {filename}"
    )

    return '', 201
