from quart import Blueprint, render_template, request
from uuid import UUID
from ddownloader.dao import http_gallery_source_dao as src_dao
from ddownloader.dao import gallery_src_download_job_dao as job_dao

sources_app = Blueprint("sources", __name__)

@sources_app.route("/", methods=["GET"])
async def all():
    sources = await src_dao.all()
    return await render_template("sources.html", sources=sources)

@sources_app.route("/download_jobs", methods=["GET"])
async def download_jobs():
    source_id_str = request.args.get("source_id")

    try:
        page_number = int(request.args.get("page", "1"))
    except ValueError:
        page_number = 1

    try:
        page_size = int(request.args.get("page_size", "30"))
    except ValueError:
        page_size = 30

    # Clamp page size to something reasonable
    if page_size < 1:
        page_size = 30
    if page_size > 200:
        page_size = 200

    source_id: UUID | None = None
    if source_id_str:
        source_id = UUID(source_id_str)

    total = await job_dao.count(source_id=source_id)
    jobs = await job_dao.page(page_number=page_number, page_size=page_size, source_id=source_id)

    total_pages = max(1, (total + page_size - 1) // page_size)
    if page_number > total_pages:
        page_number = total_pages

    return await render_template(
        "download_jobs.html",
        jobs=jobs,
        source_id=source_id_str,
        total=total,
        page=page_number,
        page_size=page_size,
        total_pages=total_pages,
    )
