from abc import ABCMeta, abstractmethod
from ddownloader.models import HttpSource


class BaseDownloader(metaclass=ABCMeta):
    """
    Abstract base class for all downloaders.
    """

    @abstractmethod
    async def download(self, src: HttpSource) -> None:
        """Downloads/syncs contents for a given http source
        """
        raise NotImplementedError("Subclasses must implement this method.")
