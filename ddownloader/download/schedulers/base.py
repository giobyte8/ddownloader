from abc import ABCMeta, abstractmethod
from ddownloader.models import HttpSource


class Scheduler(metaclass=ABCMeta):
    """
    Abstract base class for download schedulers.

    A scheduler is responsible for managing the download of files from a given source.
    It handles the scheduling and execution of download tasks.
    """

    @abstractmethod
    async def schedule(self, src: HttpSource):
        """Schedules a given source for periodic download
        """
        pass

    @abstractmethod
    async def start(self):
        """Starts the scheduler in background.

        When using same process workers (eg. Asyncio, ThreadPool, etc)
        this method will start workers execution as well.
        """
        pass
