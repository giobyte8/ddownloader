import logging
from ddownloader.dao import http_gl_src_item_dao
from ddownloader.hooks import source_downloaded as src_downloaded_hook
from ddownloader.metrics.events import evt_tracker
from ddownloader.metrics.events.base import Event
from ddownloader.models import HttpGallerySource, SrcItemRemoteStatus
from .. import gdl
from .base import BaseDownloader


log = logging.getLogger(__name__)


class GalleryDownloader(BaseDownloader):

    async def download(self, src: HttpGallerySource) -> None:
        log.debug(f"Downloading source: { src.url }")
        await evt_tracker.on(Event.SRC_DL_START, src=src)

        updated_count = await http_gl_src_item_dao.update_status_by_src_id(
            src.id,
            SrcItemRemoteStatus.UNKNOWN
        )
        log.debug(f"Updated { updated_count } items to UNKNOWN status")

        await gdl.download(src)
        await src_downloaded_hook.on_source_downloaded(src)
        await evt_tracker.on(Event.SRC_DL_END, src=src)
