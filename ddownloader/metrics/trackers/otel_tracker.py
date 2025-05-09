import logging
from opentelemetry import metrics
from uuid import UUID
from ddownloader.models import HttpGallerySource
from ..events import Event, SrcDownloadEvent
from .base import EventTracker


log = logging.getLogger(__name__)


meter = metrics.get_meter(
    "ddownloader",
    version="1.0.0"
)

counter_src_download_start = meter.create_counter(
    name=SrcDownloadEvent.START,
    description=(
        "Total times an http gallery source download process"
        "has been initiated"
    ),
    unit="1"
)

counter_src_download_end = meter.create_counter(
    name=SrcDownloadEvent.END,
    description=(
        "Total times an http gallery source download process"
        "has been completed"
    ),
    unit="1"
)

counter_files_downloaded = meter.create_counter(
    name=SrcDownloadEvent.FILE_DOWNLOADED,
    description="Total files downloaded from http gallery sources",
    unit="1"
)

counter_files_skipped = meter.create_counter(
    name=SrcDownloadEvent.FILE_SKIPPED,
    description=(
        "Total files skipped from download during http gallery sources "
        "download operations"
    ),
    unit="1"
)


class OtelEventTracker(EventTracker):

    def __init__(self):
        super().__init__(name="opentelemetry")

    async def cleanup(self):
        pass

    async def on(self, evt: Event, **kwargs):
        if evt == SrcDownloadEvent.START:
            await self.on_src_download_start(**kwargs)
        elif evt == SrcDownloadEvent.END:
            await self.on_src_download_end(**kwargs)
        elif evt == SrcDownloadEvent.FILE_DOWNLOADED:
            await self.on_file_downloaded(**kwargs)
        elif evt == SrcDownloadEvent.FILE_SKIPPED:
            await self.on_file_skipped(**kwargs)

    async def on_src_download_start(self, src: HttpGallerySource) -> None:
        counter_src_download_start.add(1, {
            "src_id": str(src.id),
            "content_path": src.content_path,
            "url": str(src.url)
        })

    async def on_src_download_end(self, src: HttpGallerySource) -> None:
        counter_src_download_end.add(1, {
            "src_id": str(src.id),
            "content_path": src.content_path,
            "url": str(src.url)
        })

    async def on_file_downloaded(self, src_id: UUID, filename: str) -> None:
       counter_files_downloaded.add(1, {
           "src_id": str(src_id),
           "filename": filename
        })

    async def on_file_skipped(self, src_id: UUID, filename: str) -> None:
        counter_files_skipped.add(1, {
           "src_id": str(src_id),
           "filename": filename
        })
