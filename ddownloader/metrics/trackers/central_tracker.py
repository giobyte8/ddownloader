import logging
from uuid import UUID
from ddownloader import config as cfg
from ddownloader.models import HttpGallerySource
from ddownloader.dao import gallery_src_download_job_dao as job_dao
from ..central import notifications as ct_notif
from ..events import Event, SrcDownloadEvent
from .base import EventTracker


log = logging.getLogger(__name__)
_DL_FILES_BASE_URL = f"{ cfg.app_base_url() }/sources/download-jobs"


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

    async def on_src_download_start(self, job_id: UUID, src: HttpGallerySource) -> None:
        # msg = f"Starting download for: { src.content_path }"
        # await ct_notif.notify(msg)
        pass

    async def on_src_download_end(self, job_id: UUID, src: HttpGallerySource) -> None:
        job = await job_dao.find_by_id(job_id)
        if job is None:
            return

        # Only notify if something was downloaded
        if job.downloaded_files_count < 1:
            return

        dl_files_url = f"{ _DL_FILES_BASE_URL }/{ job.id }/downloaded_files"
        msg = (
            "*⬇ Source Downloaded*\n"
            f"`{ await self.sanitize_telegram_md(src.content_path) }`\n"
            f"{ await self.sanitize_telegram_md(str(src.url)) }\n\n"
            f"\\- Downloaded files: {job.downloaded_files_count}\n"
            f"\\- Skipped files: {job.skipped_files_count}\n\n"
            f"[View downloaded files]({ dl_files_url })"
        )
        await ct_notif.notify(msg, format='markdown')

    async def sanitize_telegram_md(self, text: str) -> str:
        """Currently, the notifications are delivered via telegram
        by 'Central', so we need to sanitize the text to avoid breaking
        the markdown formatting.

        > This should probably be taken care of in 'Central' instead.

        Args:
            text (str): Text to sanitize/escape

        Returns:
            str: Sanitized text
        """

        # Escape characters that have special meaning in Telegram Markdown
        escape_chars = r'\_*[]()~`>#+-=|{}.!'
        for char in escape_chars:
            text = text.replace(char, f'\\{char}')
        return text
