import logging
from quart import current_app as app

from ddownloader.dao import http_gallery_source_dao as src_dao
from .schedulers.aio_gl_scheduler import AIOGalleryDlScheduler


logger = logging.getLogger(__name__)


async def start():
    logger.info("Starting download service...")
    src_dl_scheduler: AIOGalleryDlScheduler = app.src_download_scheduler

    sources = await src_dao.find_by_download_enabled(True)
    for src in sources:
        await src_dl_scheduler.schedule(src)

    await src_dl_scheduler.start()
