import logging
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from ddownloader import config as cfg
from ddownloader.models import HttpGallerySource
from .base import Scheduler
from ..downloaders.gallery_downloader import GalleryDownloader


log = logging.getLogger(__name__)
gl_downloader = GalleryDownloader()


class AIOGalleryDlScheduler(Scheduler):
    """Uses apscheduler 3.x library and asyncio for workers.
    Jobs are keep in memory, no persistent storage is used.
    """

    def __init__(self):
        store = self.__prepare_job_store()
        self._scheduler = AsyncIOScheduler(jobstores={ "default": store })

    def __prepare_job_store(self) -> SQLAlchemyJobStore:
        """Prepares the job store for the scheduler.
        """

        # For details regarding how to compose URLs see:
        # https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls
        store_url = (
            f"postgresql+psycopg://{cfg.db_user()}:{cfg.db_password()}@"
            f"{cfg.db_host()}:{cfg.db_port()}/{cfg.db_name()}"
        )

        return SQLAlchemyJobStore(url=store_url)

    async def immediate(self, src: HttpGallerySource):
        """Schedules a given source to be downloaded immediately,
        without any delay or periodicity.
        """
        if not isinstance(src, HttpGallerySource):
            raise TypeError("src must be an instance of HttpGallerySource")
        log.debug("src: %s - Scheduling for immediate download", src.id)

        # Omit 'trigger' argument to execute the job immediately.
        self._scheduler.add_job(
            gl_downloader.download,
            id=f"immediate-{ src.id }",

            # Args for the 'gl_downloader.download' function.
            args=[src],
            replace_existing=True,
        )

    async def schedule(self, src: HttpGallerySource):
        """Schedules a given source for periodic download based on its
        `download_schedule` attribute. \

        If a job with the same id already exists, it will be replaced with
        the new one. This prevents jobs duplication across application runs.
        """
        if not isinstance(src, HttpGallerySource):
            raise TypeError("src must be an instance of HttpGallerySource")

        log.info("src: %s - Scheduling with crontab: %s", src.id, src.download_schedule)

        # See: https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html#examples
        self._scheduler.add_job(
            gl_downloader.download,
            CronTrigger.from_crontab(src.download_schedule),
            id=str(src.id),

            # The old job with same id will be replaced with new one.
            #  This guarantees the job doesn't get duplicated across
            #  application runs or if same source is scheduled multiple times.
            replace_existing=True,
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
            log.warning("Gallery download Scheduler is already running")
