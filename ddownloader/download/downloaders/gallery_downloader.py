import logging
from ddownloader.dao import http_gl_src_item_dao
from ddownloader.hooks import source_downloaded
from ddownloader.models import HttpGallerySource, SrcItemRemoteStatus
from .. import gdl
from .base import BaseDownloader


logger = logging.getLogger(__name__)


class GalleryDownloader(BaseDownloader):

    async def download(self, src: HttpGallerySource) -> None:
        logger.debug(f"Downloading source: { src.url }")

        updated_count = await http_gl_src_item_dao.update_status_by_src_id(
            src.id,
            SrcItemRemoteStatus.UNKNOWN
        )
        logger.debug(f"Updated { updated_count } items to UNKNOWN status")

        await gdl.download(src)
        await source_downloaded.on_source_downloaded(src)
