from quart import Blueprint, render_template, request, abort, redirect, url_for, current_app as app
from pydantic import ValidationError
from uuid import UUID
from ddownloader import config as cfg
from ddownloader.dao import http_gallery_source_dao as src_dao
from ddownloader.dao import gallery_src_download_job_dao as job_dao
from ddownloader.dao import download_job_downloaded_file_dao as downloaded_file_dao
from ddownloader.models import HttpGallerySource
from ddownloader.web.form_models import CreateSourceForm

sources_app = Blueprint("sources", __name__)

@sources_app.route("/", methods=["GET"])
async def all():
    sources = await src_dao.all()
    return await render_template("sources.html", sources=sources)


@sources_app.route("/new", methods=["GET"])
async def new_source():
    return await render_template(
        "sources/new.html",
        errors={},
        form={"download_schedule": "0 0 * * SUN"},
        galleries_path=cfg.galleries_path(),
    )


@sources_app.route("/", methods=["POST"])
async def create_source():
    form = await request.form
    errors = {}

    # Stage 1: format / constraint validation (sync, Pydantic)
    try:
        data = CreateSourceForm.model_validate({
            **form,
            "sync_remote_deletes": "sync_remote_deletes" in form,
            "download_enabled": "download_enabled" in form,
        })
    except ValidationError as e:
        for err in e.errors():
            field = err["loc"][0] if err["loc"] else "__all__"
            if field not in errors:
                errors[field] = err["msg"].removeprefix("Value error, ")

    # Stage 2: DB-dependent validation (async) — only when format is clean
    if not errors:
        if await src_dao.exists_by_url(str(data.url)):
            errors["url"] = "A source with this URL already exists"

    if errors:
        return await render_template(
            "sources/new.html",
            errors=errors,
            form=form,
            galleries_path=cfg.galleries_path(),
        ), 422

    source = HttpGallerySource(
        url=data.url,
        content_path=data.content_path,
        sync_remote_deletes=data.sync_remote_deletes,
        download_schedule=data.download_schedule,
        download_enabled=data.download_enabled,
    )
    await src_dao.create(source)

    if source.download_enabled and source.download_schedule:
        await app.src_download_scheduler.schedule(source)

    return redirect(url_for("sources.all"))

@sources_app.route("/<uuid:src_id>/download_jobs", methods=["POST"])
async def download_immediately(src_id: UUID):
    src = await src_dao.find_by_id(src_id)
    if not src:
        abort(404, description="Source not found")

    # Schedule the source for immediate download
    await app.src_download_scheduler.immediate(src)

    return redirect(url_for("sources.download_jobs", source_id=src_id))


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

@sources_app.route("/download_jobs/<job_id>/downloaded_files", methods=["GET"])
async def download_job_downloaded_files(job_id: str):
    try:
        job_id = UUID(job_id)
    except ValueError:
        abort(400, description="Invalid job_id")

    try:
        page_number = int(request.args.get("page", "1"))
    except ValueError:
        page_number = 1

    try:
        page_size = int(request.args.get("page_size", "30"))
    except ValueError:
        page_size = 30

    if page_size < 1:
        page_size = 30
    if page_size > 200:
        page_size = 200

    job = await job_dao.find_by_id(job_id)
    total = await downloaded_file_dao.count(job_id=job_id)
    files = await downloaded_file_dao.page(
        job_id=job_id,
        page_number=page_number,
        page_size=page_size
    )

    total_pages = max(1, (total + page_size - 1) // page_size)
    if page_number > total_pages:
        page_number = total_pages

    return await render_template(
        "downloaded_files.html",
        job_id=str(job_id),
        job=job,
        files=files,
        total=total,
        page=page_number,
        page_size=page_size,
        total_pages=total_pages,
    )
