import logging
from ddownloader.models import HttpGallerySource
from .base import BaseDownloader


logger = logging.getLogger(__name__)


class GalleryDownloader(BaseDownloader):

    async def download(self, src: HttpGallerySource) -> None:
        logger.debug(f"Downloading gallery from {src.url}")
