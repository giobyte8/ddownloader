from pydantic import BaseModel, HttpUrl
from uuid import UUID, uuid4


class HttpSource(BaseModel):
    id: UUID = uuid4()
    url: HttpUrl


class HttpSingleFileSource(HttpSource):
    dst_path: str


class HttpGallerySource(HttpSource):
    content_path: str
    sync_remote_deletes: bool = True