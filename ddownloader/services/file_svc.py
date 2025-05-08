import logging
import os
from opentelemetry import trace
from uuid import UUID
import ddownloader.config as cfg
from ddownloader.dao import http_gallery_source_dao as src_dao
from ddownloader.models import HttpGallerySourceItem


logger = logging.getLogger(__name__)
tracer = trace.get_tracer(cfg.otel_svc_name())


@tracer.start_as_current_span("file_svc.content_path")
async def content_path(src_id: UUID) -> str:
    """Computes abs path to content folder for given source.

    Args:
        source (HttpGallerySource): Gallery source.

    Returns:
        str: Abs path to content folder.
    """
    # TODO Implement cache and compare performance
    # cached_path = cache_svc.source_content_path(src.id)
    # if cached_path:
    #     return cached_path

    src = await src_dao.find_by_id(src_id)
    if not src:
        raise ValueError(f"Source with id {src.id} not found")

    path = os.path.join(cfg.galleries_path(), src.content_path)
    # TODO Save to cache
    return path


async def file_path(item: HttpGallerySourceItem) -> str:
    """Computes the abs path for file of given item.

    Args:
        item (HttpGallerySourceItem): Gallery item.

    Returns:
        str: Abs path to item file.
    """
    return os.path.join(
        await content_path(item.source_id),
        item.filename
    )

async def delete_file(item: HttpGallerySourceItem) -> None:
    """Deletes file of given item.

    Args:
        item (HttpGallerySourceItem): Gallery item.
    """
    path = await file_path(item)
    if os.path.exists(path):
        os.remove(path)
        logger.debug(f"File {path} deleted")
    else:
        logger.warning(f"File {path} not found")