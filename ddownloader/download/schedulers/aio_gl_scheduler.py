import logging
import ddownloader.config as cfg
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from ddownloader.models import HttpGallerySource
from .base import Scheduler
from ..downloaders.gallery_downloader import GalleryDownloader


logger = logging.getLogger(__name__)
gl_downloader = GalleryDownloader()
crontab = cfg.gl_sync_crontab()
jitter = cfg.gl_sync_jitter()


class AIOGalleryDlScheduler(Scheduler):
    """Uses apscheduler 3.x library and asyncio for workers.
    Jobs are keep in memory, no persistent storage is used.
    """

    def __init__(self):
        self._scheduler = AsyncIOScheduler()

    async def schedule(self, src: HttpGallerySource):
        """Schedules a given source for periodic download
        """
        if not isinstance(src, HttpGallerySource):
            raise TypeError("src must be an instance of HttpGallerySource")

        logger.debug(f"Scheduling {src.id} with crontab: {crontab} and jitter: {jitter}")

        # See: https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html#examples
        self._scheduler.add_job(
            gl_downloader.download,
            CronTrigger.from_crontab(crontab),
            args=[src],
            jitter=jitter,
        )

    async def start(self):
        """Starts the scheduler in background.
        """
        if not self._scheduler.running:
            self._scheduler.start()
        else:
            logger.warning("Gallery download Scheduler is already running")
