import datetime
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
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

        # TODO Tune up parameters below to ensure sequential download of sources
        # Next run = now + 1 second
        next_run = datetime.datetime.now() + datetime.timedelta(seconds=1)
        self._scheduler.add_job(
            func=gl_downloader.download,
            args=[src],
            trigger='interval',     # TODO: Update to every night
            seconds=30,             # TODO: make this configurable
            misfire_grace_time=60,
            #next_run_time=next_run
        )

    async def start(self):
        """Starts the scheduler in background.
        """
        if not self._scheduler.running:
            self._scheduler.start()
            logger.init("Galleries download Scheduler started")
        else:
            logger.warning("Gallery download Scheduler is already running")
