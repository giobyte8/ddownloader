import logging
from ddownloader.models import HttpGallerySource
from .tortoise.models import DBHttpGallerySource


logger = logging.getLogger(__name__)


async def all() -> list[HttpGallerySource]:
    """
    Get all HTTP sources from the database.

    Returns:
        list[DBHttpSource]: List of all HTTP sources.
    """
    db_sources = await DBHttpGallerySource.all()

    sources = []
    for db_src in db_sources:
        sources.append(HttpGallerySource(
            id=db_src.id,
            url=db_src.url,
            content_path=db_src.content_path,
            sync_remote_deletes=db_src.sync_remote_deletes,
        ))

    return sources
