from enum import Enum
from pydantic import BaseModel, HttpUrl
from uuid import UUID, uuid4


class HttpSource(BaseModel):
    id: UUID = uuid4()
    url: HttpUrl


class HttpSingleFileSource(HttpSource):
    dst_path: str


class HttpGallerySource(HttpSource):
    content_path: str
    sync_remote_deletes: bool
    download_schedule: str


class SrcItemRemoteStatus(Enum):
    FOUND = "Found"
    NOT_FOUND = "Not found"
    UNKNOWN = "Unknown"


class HttpGallerySourceItem(BaseModel):
    id: UUID = uuid4()
    source_id: UUID
    filename: str
    remote_status: SrcItemRemoteStatus
