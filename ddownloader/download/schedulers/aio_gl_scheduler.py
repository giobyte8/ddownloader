import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from ddownloader.models import HttpGallerySource
from .base import Scheduler
from ..downloaders.gallery_downloader import GalleryDownloader


logger = logging.getLogger(__name__)
gl_downloader = GalleryDownloader()


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

        logger.debug(f"Scheduling {src.id} with crontab: { src.download_schedule }")

        # See: https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html#examples
        self._scheduler.add_job(
            gl_downloader.download,
            CronTrigger.from_crontab(src.download_schedule),
            args=[src],

            # Will start the job with a delay of -60 to +60 seconds
            # from the scheduled time. This is to prevent spikes in requests
            # where multiple sources are scheduled at the same time.
            jitter=60,
        )

    async def start(self):
        """Starts the scheduler in background.
        """
        if not self._scheduler.running:
            self._scheduler.start()
        else:
            logger.warning("Gallery download Scheduler is already running")
