import logging
from ddownloader.dao import http_gallery_source_dao as src_dao
from .schedulers.aio_gl_scheduler import AIOGalleryDlScheduler


logger = logging.getLogger(__name__)


async def start():
    logger.info("Starting download service...")
    scheduler = AIOGalleryDlScheduler()

    sources = await src_dao.all()
    for src in sources:
        logger.debug(f"Scheduling source '{src.content_path}' for download")
        await scheduler.schedule(src)

    await scheduler.start()
