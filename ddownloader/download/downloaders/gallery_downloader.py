import logging
from opentelemetry import trace
from ddownloader import config as cfg
from ddownloader.dao import http_gl_src_item_dao
from ddownloader.hooks import source_downloaded as src_downloaded_hook
from ddownloader.metrics.events import SrcDownloadEvent
from ddownloader.metrics.tracker import event_hub
from ddownloader.models import HttpGallerySource, SrcItemRemoteStatus

from .. import gdl
from .base import BaseDownloader


log = logging.getLogger(__name__)
tracer = trace.get_tracer(cfg.otel_svc_name())


class GalleryDownloader(BaseDownloader):

    @tracer.start_as_current_span("gl_downloader.download")
    async def download(self, src: HttpGallerySource) -> None:
        span = trace.get_current_span()
        span.set_attribute("source.id", str(src.id))
        span.set_attribute("source.url", str(src.url))
        span.set_attribute("source.content_path", str(src.content_path))

        log.debug(f"Downloading source: { src.url }")
        await event_hub.on(SrcDownloadEvent.START, src=src)

        updated_count = await http_gl_src_item_dao.update_status_by_src_id(
            src.id,
            SrcItemRemoteStatus.UNKNOWN
        )
        log.debug(f"Updated { updated_count } items to UNKNOWN status")

        await gdl.download(src)
        await src_downloaded_hook.on_source_downloaded(src)
        await event_hub.on(SrcDownloadEvent.END, src=src)
