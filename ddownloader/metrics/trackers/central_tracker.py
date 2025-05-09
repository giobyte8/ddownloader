from ddownloader.models import HttpGallerySource
from ..central import notifications as ct_notif
from ..events import Event, SrcDownloadEvent
from .base import EventTracker


class CentralEventTracker(EventTracker):
    """Tracks events that should be posted/notified to \
    Central service
    """

    def __init__(self):
        super().__init__(name="central")

    async def cleanup(self) -> None:
        await ct_notif.cleanup()

    async def on(self, evt: Event, **kwargs) -> None:
        if evt == SrcDownloadEvent.START:
            await self.on_src_download_start(**kwargs)
        elif evt == SrcDownloadEvent.END:
            await self.on_src_download_end(**kwargs)

    async def on_src_download_start(self, src: HttpGallerySource) -> None:
        msg = f"Starting download for: { src.content_path }"
        await ct_notif.notify(msg)

    async def on_src_download_end(self, src: HttpGallerySource) -> None:
        msg = f"Download complete for: { src.content_path }"
        await ct_notif.notify(msg)
