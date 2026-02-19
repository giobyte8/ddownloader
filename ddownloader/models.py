from enum import Enum
from pydantic import BaseModel, HttpUrl
from uuid import UUID, uuid4
from datetime import datetime


class HttpSource(BaseModel):
    id: UUID = uuid4()
    url: HttpUrl


class HttpSingleFileSource(HttpSource):
    dst_path: str


class HttpGallerySource(HttpSource):
    content_path: str
    sync_remote_deletes: bool
    download_schedule: str
    download_enabled: bool


class SrcItemRemoteStatus(Enum):
    FOUND = "Found"
    NOT_FOUND = "Not found"
    UNKNOWN = "Unknown"


class HttpGallerySourceItem(BaseModel):
    id: UUID = uuid4()
    source_id: UUID
    filename: str
    remote_status: SrcItemRemoteStatus


class GallerySrcDownloadJob(BaseModel):
    id: UUID = uuid4()
    source_id: UUID
    started_at: datetime | None = None
    completed_at: datetime | None = None

    source: HttpGallerySource | None = None
    downloaded_files_count: int = 0
    skipped_files_count: int = 0


class DownloadJobDownloadedFile(BaseModel):
    id: UUID = uuid4()
    job_id: UUID
    src_item_id: UUID
    created_at: datetime | None = None

    src_item: HttpGallerySourceItem | None = None


class DownloadJobSkippedFile(BaseModel):
    id: UUID = uuid4()
    job_id: UUID
    src_item_id: UUID
    created_at: datetime | None = None
