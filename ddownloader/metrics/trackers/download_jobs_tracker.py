"""Keeps track of each download job for each source and the
downloaded and skipped files for each job.

This tracker persists download-job monitoring data into the database.
"""

from uuid import UUID
from ddownloader.models import (
    HttpGallerySource,
    GallerySrcDownloadJob,
    DownloadJobDownloadedFile,
    DownloadJobSkippedFile,
)
from ddownloader.dao import gallery_src_download_job_dao as job_dao
from ddownloader.dao import download_job_downloaded_file_dao as downloaded_dao
from ddownloader.dao import download_job_skipped_file_dao as skipped_dao
from ..events import Event, SrcDownloadEvent
from .base import EventTracker


class DownloadJobsTracker(EventTracker):
    def __init__(self):
        super().__init__(name="download_jobs")

    async def cleanup(self) -> None:
        pass

    async def on(self, evt: Event, **kwargs) -> None:
        if evt == SrcDownloadEvent.START:
            await self.on_src_download_start(**kwargs)
        elif evt == SrcDownloadEvent.END:
            await self.on_src_download_end(**kwargs)
        elif evt == SrcDownloadEvent.FILE_DOWNLOADED:
            await self.on_file_downloaded(**kwargs)
        elif evt == SrcDownloadEvent.FILE_SKIPPED:
            await self.on_file_skipped(**kwargs)

    async def on_src_download_start(
        self,
        job_id: UUID,
        src: HttpGallerySource
    ) -> None:
        job = GallerySrcDownloadJob(
            id=job_id,
            source_id=src.id
        )
        await job_dao.upsert(job)

    async def on_src_download_end(
        self,
        job_id: UUID,
        src: HttpGallerySource
    ) -> None:
        # Mark job as completed (uses utcnow)
        await job_dao.mark_completed(job_id)

    async def on_file_downloaded(
        self,
        job_id: UUID,
        src_id: UUID,
        src_item_id: UUID,
        filename: str
    ) -> None:
        await downloaded_dao.insert(DownloadJobDownloadedFile(
            job_id=job_id,
            src_item_id=src_item_id,
        ))

    async def on_file_skipped(
        self,
        job_id: UUID,
        src_id: UUID,
        src_item_id: UUID,
        filename: str,
    ) -> None:
        await skipped_dao.insert(DownloadJobSkippedFile(
            job_id=job_id,
            src_item_id=src_item_id,
        ))
        pass
