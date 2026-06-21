import logging
from datetime import datetime
from uuid import UUID, uuid4
from tortoise.expressions import Subquery, RawSQL

from ddownloader.models import HttpGallerySource
from .tortoise.models import DBHttpGallerySource, DBAPSchedulerJob


logger = logging.getLogger(__name__)


async def find_by_id(src_id: str) -> HttpGallerySource | None:
    """
    Find HTTP source by ID.

    Args:
        src_id (str): Source ID.

    Returns:
        HttpGallerySource | None: Source object or None if not found.
    """
    db_src = await DBHttpGallerySource.get_or_none(id=src_id)
    if db_src is None:
        return None

    return HttpGallerySource(
        id=db_src.id,
        url=db_src.url,
        content_path=db_src.content_path,
        sync_remote_deletes=db_src.sync_remote_deletes,
        download_schedule=db_src.download_schedule,
        download_enabled=db_src.download_enabled,
    )


async def find_by_download_enabled(enabled: bool) -> list[HttpGallerySource]:
    """
    Find HTTP sources by download enabled status.

    Args:
        enabled (bool): Download enabled status.

    Returns:
        list[HttpGallerySource]: List of sources with the specified download enabled status.
    """
    db_sources = await DBHttpGallerySource.filter(download_enabled=enabled)

    sources = []
    for db_src in db_sources:
        sources.append(HttpGallerySource(
            id=db_src.id,
            url=db_src.url,
            content_path=db_src.content_path,
            sync_remote_deletes=db_src.sync_remote_deletes,
            download_schedule=db_src.download_schedule,
            download_enabled=db_src.download_enabled,
        ))

    return sources


async def all() -> list[HttpGallerySource]:
    """
    Get all HTTP sources from the database.

    Returns:
        list[HttpGallerySource]: List of all HTTP sources.
    """
    db_sources = await DBHttpGallerySource\
        .annotate(
            job_next_run_time=Subquery(
                DBAPSchedulerJob\
                    .filter(id=RawSQL('http_gallery_source.id::text'))\
                    .limit(1)\
                    .values('next_run_time')
            )
        )\
        .all()

    sources = []
    for db_src in db_sources:
        next_run_time = None
        if db_src.job_next_run_time:
            try:
                next_run_time = datetime.fromtimestamp(db_src.job_next_run_time)
            except Exception as e:
                logger.warning(
                    f"Failed to parse job_next_run_time for source {db_src.id}: {e}"
                )

        sources.append(HttpGallerySource(
            id=db_src.id,
            url=db_src.url,
            content_path=db_src.content_path,
            sync_remote_deletes=db_src.sync_remote_deletes,
            download_schedule=db_src.download_schedule,
            download_enabled=db_src.download_enabled,
            job_next_run_time=next_run_time,
        ))

    return sources


async def exists_by_url(url: str) -> bool:
    return await DBHttpGallerySource.filter(url=url).exists()


async def exists_by_url_excluding(url: str, exclude_id: UUID) -> bool:
    return await DBHttpGallerySource.filter(url=url).exclude(id=exclude_id).exists()


async def create(source: HttpGallerySource) -> HttpGallerySource:
    db_src = await DBHttpGallerySource.create(
        id=uuid4(),
        url=str(source.url),
        content_path=source.content_path,
        sync_remote_deletes=source.sync_remote_deletes,
        download_schedule=source.download_schedule,
        download_enabled=source.download_enabled,
    )
    source.id = db_src.id
    return source


async def update(source: HttpGallerySource) -> HttpGallerySource:
    await DBHttpGallerySource.filter(id=source.id).update(
        url=str(source.url),
        content_path=source.content_path,
        sync_remote_deletes=source.sync_remote_deletes,
        download_schedule=source.download_schedule,
        download_enabled=source.download_enabled,
    )
    return source
