import logging
from ddownloader.models import HttpGallerySource
from .schedulers.aio_gl_scheduler import AIOGalleryDlScheduler


logger = logging.getLogger(__name__)


async def start(sources: list[HttpGallerySource]):
    logger.info("Starting download service...")
    scheduler = AIOGalleryDlScheduler()

    for src in sources:
        logger.debug(f"Scheduling source '{src.id}' for download")
        await scheduler.schedule(src)

    await scheduler.start()
