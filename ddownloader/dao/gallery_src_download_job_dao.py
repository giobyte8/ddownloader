from datetime import datetime, timezone
from opentelemetry import trace
from uuid import UUID
from ddownloader import config as cfg
from ddownloader.models import GallerySrcDownloadJob, HttpGallerySource
from tortoise.functions import Count
from .tortoise.models import DBGallerySrcDownloadJob


tracer = trace.get_tracer(cfg.otel_svc_name())


@tracer.start_as_current_span("download_job_dao.all")
async def all() -> list[GallerySrcDownloadJob]:
    db_jobs = await DBGallerySrcDownloadJob.all()

    jobs: list[GallerySrcDownloadJob] = []
    for db_job in db_jobs:
        jobs.append(GallerySrcDownloadJob(
            id=db_job.id,
            source_id=db_job.source_id,
            started_at=db_job.started_at,
            completed_at=db_job.completed_at,
        ))

    return jobs


@tracer.start_as_current_span("download_job_dao.find_by_source_id")
async def find_by_source_id(source_id: UUID) -> list[GallerySrcDownloadJob]:
    db_jobs = await DBGallerySrcDownloadJob.filter(source_id=source_id).all()

    jobs: list[GallerySrcDownloadJob] = []
    for db_job in db_jobs:
        jobs.append(GallerySrcDownloadJob(
            id=db_job.id,
            source_id=db_job.source_id,
            started_at=db_job.started_at,
            completed_at=db_job.completed_at,
        ))

    return jobs


@tracer.start_as_current_span("download_job_dao.upsert")
async def upsert(job: GallerySrcDownloadJob) -> GallerySrcDownloadJob:
    db_job, is_new = await DBGallerySrcDownloadJob.get_or_create(
        id=job.id,
        defaults={
            "source_id": job.source_id,
        }
    )

    if is_new:
        job.id = db_job.id
        job.started_at = db_job.started_at
        return job

    await db_job.update_from_dict({
        "source_id": job.source_id,
        "started_at": job.started_at,
        "completed_at": job.completed_at,
    }).save()

    return job


@tracer.start_as_current_span("download_job_dao.count")
async def count(source_id: UUID | None = None) -> int:
    qs = DBGallerySrcDownloadJob.all()
    if source_id is not None:
        qs = qs.filter(source_id=source_id)
    return await qs.count()


@tracer.start_as_current_span("download_job_dao.page")
async def page(
    page_number: int,
    page_size: int = 30,
    source_id: UUID | None = None,
) -> list[GallerySrcDownloadJob]:
    if page_number < 1:
        page_number = 1
    if page_size < 1:
        page_size = 30

    offset = (page_number - 1) * page_size

    qs = DBGallerySrcDownloadJob.all()
    if source_id is not None:
        qs = qs.filter(source_id=source_id)

    db_jobs = await (
        qs.annotate(
            downloaded_files_count=Count("downloaded_files", distinct=True),
            skipped_files_count=Count("skipped_files", distinct=True),
        )
        .group_by("id")
        .prefetch_related("source")
        .order_by("-started_at")
        .offset(offset)
        .limit(page_size)
    )

    jobs: list[GallerySrcDownloadJob] = []
    for db_job in db_jobs:
        source = None
        if getattr(db_job, "source", None) is not None:
            source = HttpGallerySource(
                id=db_job.source.id,
                url=db_job.source.url,
                content_path=db_job.source.content_path,
                sync_remote_deletes=db_job.source.sync_remote_deletes,
                download_schedule=db_job.source.download_schedule,
                download_enabled=db_job.source.download_enabled,
            )

        jobs.append(GallerySrcDownloadJob(
            id=db_job.id,
            source_id=db_job.source_id,
            started_at=db_job.started_at,
            completed_at=db_job.completed_at,
            source=source,
            downloaded_files_count=int(getattr(db_job, "downloaded_files_count", 0) or 0),
            skipped_files_count=int(getattr(db_job, "skipped_files_count", 0) or 0),
        ))

    return jobs


@tracer.start_as_current_span("download_job_dao.find_by_id")
async def find_by_id(job_id: UUID) -> GallerySrcDownloadJob | None:
    db_job = await DBGallerySrcDownloadJob\
        .get_or_none(id=job_id)\
        .prefetch_related("source")
    if db_job is None:
        return None

    source = None
    if getattr(db_job, "source", None) is not None:
        source = HttpGallerySource(
            id=db_job.source.id,
            url=db_job.source.url,
            content_path=db_job.source.content_path,
            sync_remote_deletes=db_job.source.sync_remote_deletes,
            download_schedule=db_job.source.download_schedule,
            download_enabled=db_job.source.download_enabled,
        )

    return GallerySrcDownloadJob(
        id=db_job.id,
        source_id=db_job.source_id,
        started_at=db_job.started_at,
        completed_at=db_job.completed_at,
        source=source,
    )


@tracer.start_as_current_span("download_job_dao.mark_completed")
async def mark_completed(job_id: UUID) -> int:
    # Uses DB default timezone-aware NOW() equivalent on the application
    # side by setting to current timestamp via Tortoise's update method
    # and Postgres TIMESTAMPTZ.

    return await DBGallerySrcDownloadJob\
        .filter(id=job_id)\
        .update(completed_at=datetime.now(timezone.utc))
