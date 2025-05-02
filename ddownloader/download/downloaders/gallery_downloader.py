import logging
from ddownloader.dao import http_gl_src_item_dao
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
        # TODO: Implement gdl post download hook to remove 'Unkown' items if 'applicable' (Were not found)
        #       or just mark them as 'Not Found' if source.sync_remote_deletes is set to False
