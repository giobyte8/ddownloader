import logging
from ddownloader import config as cfg
from ddownloader.models import HttpGallerySource
from .base import Event, EventTracker
from ..central import notifications as ct_notif


log = logging.getLogger(__name__)


class CentralEventTracker(EventTracker):
    """
    Event tracker that sends events to central.
    """

    def __init__(self):
        super().__init__(name="central")

    async def cleanup(self) -> None:
        await ct_notif.cleanup()

    async def on(self, evt: Event, **kwargs) -> None:
        if not cfg.ct_monitoring_enabled():
            log.debug(f"{ self.name } event tracking is disabled")
            return
        await super().on(evt, **kwargs)

    async def on_src_dl_start(self, src: HttpGallerySource) -> None:
        msg = f"Starting download for: { src.content_path }"
        await ct_notif.notify(msg)

    async def on_src_dl_end(self, src: HttpGallerySource) -> None:
        msg = f"Download complete for: { src.content_path }"
        await ct_notif.notify(msg)
