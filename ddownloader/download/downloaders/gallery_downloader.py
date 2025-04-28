import logging
from ddownloader.models import HttpGallerySource
from .. import gdl
from .base import BaseDownloader


logger = logging.getLogger(__name__)


class GalleryDownloader(BaseDownloader):

    async def download(self, src: HttpGallerySource) -> None:
        logger.debug(f"Downloading gallery from {src.url}")
        await gdl.download(src)
