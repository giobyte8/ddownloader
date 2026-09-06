from cron_descriptor import get_description
from enum import Enum
from pydantic import BaseModel, HttpUrl
from pathlib import Path
from uuid import UUID, uuid4
from datetime import datetime


def _path_to_human(path: str) -> str:
    """Takes a file system path and formats its last segment to make it
    human friendly by: \
        1. Taking the last segment of the path \
        2. Replacing '-' and '_' with spaces \
        3. Capitalizing if all letters are lowercase

    Args:
        path (str): File system path to format

    Returns:
        str: Human friendly representation
    """
    if not path:
        return ""

    # Use pathlib to get the last path segment (OS-native semantics).
    last_segment = Path(path).name

    # Replace separators '-' and '_' with spaces and trim whitespace.
    name = last_segment.replace("-", " ").replace("_", " ").strip()
    if not name:
        # If replacing delimiters yields only empty/space, return the
        # original last segment instead of an empty string.
        return last_segment

    # If all alphabetic characters are lowercase, capitalize the result.
    letters = [c for c in name if c.isalpha()]
    if letters and all(c.islower() for c in letters):
        name = name.capitalize()

    return name

class HttpSource(BaseModel):
    id: UUID = uuid4()
    url: HttpUrl


class HttpSingleFileSource(HttpSource):
    dst_path: str


class HttpGallerySource(HttpSource):
    content_path: str
    sync_remote_deletes: bool
    download_schedule: str | None = None
    download_enabled: bool

    # Run time for next scheduled download job, if any.
    #  Timezone depends on how apscheduler store it.
    #  By default it uses local timezone
    job_next_run_time: datetime | None = None

    @property
    def name(self) -> str:
        """Returns a human-readable name for the source,
        derived from the last segment of `content_path`.
        """
        return _path_to_human(self.content_path)

    @property
    def download_schedule_description(self) -> str | None:
        if not self.download_schedule:
            return None
        return get_description(self.download_schedule)


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

class Directory(BaseModel):
    """A DTO representing a directory holding media galleries content
    and the sources that feed content into it.
    """
    path: str
    sources: list[HttpGallerySource] = []

    @property
    def name(self) -> str:
        """Computes a human-readable representation of this directory,
        derived from the last segment of its `path`.
        """
        return _path_to_human(self.path)
