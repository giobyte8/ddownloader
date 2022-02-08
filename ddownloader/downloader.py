import os
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Callable

import requests
from requests.exceptions import RequestException
from ddownloader.errors import MetadataReqError


class DownloadStatus(Enum):
    QUEUED = "Queued"

    IN_PROGRESS = "In Progress"
    PAUSED = "Paused"
    COMPLETED = "Completed"
    FAILED = "Failed"

@dataclass
class DownloadTask:
    url: str
    target_path: str

    id: int = 0
    total_size: int = 0
    downloaded_size: int = 0
    status: DownloadStatus = DownloadStatus.QUEUED
    file_hash: str = None
    err_message: str = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'url': self.url,
            'target_path': self.target_path,
            'total_size': self.total_size,
            'downloaded_size': self.downloaded_size,
            'status': self.status.value,
            'file_hash': self.file_hash,
            'err_message': self.err_message
        }

    def valid_for_download(self) -> bool:
        """Checks if download task is valid for be started or resumed

        Raises:
            DownloadNotQueuedError: When status is not 'Queued'
            DownloadAlreadyInProgressError: When status is 'In progress'

        Returns:
            bool: True if download tasks state is valid and
                download can proceeed
        """
        if self.status == DownloadStatus.IN_PROGRESS:
            raise DownloadAlreadyInProgressError()

        elif self.status != DownloadStatus.QUEUED:
            raise DownloadNotQueuedError()

        return True

class TargetPathAlreadyExistsError(Exception):
    def __init__(self, target_path: str) -> None:
        self.message = "Destination file path already exists: {}".format(
            target_path
        )

        super().__init__(self.message)

class DownloadNotQueuedError(Exception):
    def __init__(self) -> None:
        super().__init__("Download task is not ready for execution")

class DownloadAlreadyInProgressError(Exception):
    def __init__(self) -> None:
        super().__init__("Download is already in progress")

@dataclass
class UrlMetadata:
    url: str
    content_disposition: str = ''
    content_length: int = 0
    content_type: str = ''
    server: str = ''
    proposed_file_name: str = ''

    def to_dict(self) -> dict:
        return {
            'url': self.url,
            'content_disposition': self.content_disposition,
            'content_length': self.content_length,
            'content_type': self.content_type,
            'server': self.server,
            'proposed_file_name': self.proposed_file_name
        }

    def compute_file_name(self) -> str:
        filename = ''

        if self.content_disposition:
            parts = self.content_disposition.split(';')
            for part in parts:
                if part.startswith('filename='):
                    filename = part                  \
                        .replace('filename=', '', 1) \
                        .strip("\"")

        if not filename:
            filename = os.path.basename(self.url)

        if not filename:
            filename = str(uuid.uuid4())

        if not '.' in filename:
            if self.content_type == 'image/jpeg':
                filename += '.jpeg'

            if self.content_type == 'image/jpg':
                filename += '.jpg'

            if self.content_type == 'image/png':
                filename += '.png'

        self.proposed_file_name = filename


def metadata(url: str) -> UrlMetadata:
    try:
        res = requests.head(url, timeout=5, allow_redirects=True)
        res.raise_for_status()
    except RequestException as err:
        raise MetadataReqError(str(err)) from err

    url_meta = UrlMetadata(url)

    if 'Content-Disposition' in res.headers:
        url_meta.content_disposition = res.headers['Content-Disposition']

    if 'Content-Length' in res.headers:
        url_meta.content_length = res.headers['Content-Length']

    if 'Content-Type' in res.headers:
        url_meta.content_type = res.headers['Content-Type']

    if 'Server' in res.headers:
        url_meta.server = res.headers['Server']

    url_meta.compute_file_name()
    return url_meta


def download(
    dtask: DownloadTask,
    on_update: Callable,
    reload_status: Callable
) -> None:
    """Starts or resumes given download task if it is
    ready for download. See 'DownloadTask.valid_for_download'

    Args:
        dtask (str): Download job descriptor
        on_update (Callable): Callback to invoke constantly during
            download progress or status changes
        reload_status (Callable): Callback to invoke in order to ask for
            external refresh of download status. Use this for
            check if download was externaly paused
    """
    chunk_size = 1024 * 1024 * 5  # 5MB

    if dtask.valid_for_download():

        # Set status as 'In progress'
        dtask.status = DownloadStatus.IN_PROGRESS
        on_update()

        with _make_request(dtask) as res:
            res.raise_for_status()

            # Get file total size from response headers
            if res.headers['Content-length']:
                dtask.total_size = int(res.headers['Content-length'])
                if dtask.downloaded_size > 0:
                    dtask.total_size += dtask.downloaded_size

            # Append bytes if file already exists, otherwise write
            file_mode = 'ab' if os.path.exists(dtask.target_path) else 'wb'
            with open(dtask.target_path, file_mode) as target:
                for chunk in res.iter_content(chunk_size=chunk_size):

                    # Ensure chunk is not empty
                    if chunk:
                        target.write(chunk)
                        dtask.downloaded_size += len(chunk)

                    # Reload external status before update downloaded size
                    # to avoid override possible external changes
                    reload_status()
                    on_update()

                    # Stop download if status was externally changed
                    if dtask.status != DownloadStatus.IN_PROGRESS:
                        res.close()
                        return

                if dtask.downloaded_size == dtask.total_size:
                    dtask.status = DownloadStatus.COMPLETED
                else:
                    dtask.status = DownloadStatus.FAILED
                on_update()


def _make_request(dtask: DownloadTask):
    """Constructs download request for given task.
    If target path already exists, request will fetch only remaining
    bytes using the 'Range' header

    Args:
        dtask (DownloadTask): Download job to execute

    Returns:
        [type]: Http request with stream mode enabled
    """
    starting_byte = 0
    if os.path.exists(dtask.target_path):
        starting_byte = os.path.getsize(dtask.target_path)

    # Skip previously downloaded bytes when applicable.
    # e.g. like when resuming download
    range_header = {'Range': f'bytes={starting_byte}-'}
    headers = range_header if starting_byte else None

    return requests.get(
        dtask.url,
        stream=True,
        headers=headers,
        timeout=60 # seconds
    )

# def _refresh(dtask: DownloadTask):
#     dtask.status = DownloadStatus.IN_PROGRESS

# dtask = DownloadTask(
#     url="http://192.168.1.103:8082/Downloads/Cruella.2021.1080p-dual-cast-cine-calidad.com.mp4",
#     target_path="movie.mkv"
# )

# try:
#     download(
#         dtask,
#         lambda: print("{}: {} MB of {} MB".format(
#             dtask.status,
#             round(dtask.downloaded_size / 1024 / 1024),
#             round(dtask.total_size / 1024 / 1024)
#         )),
#         lambda: _refresh(dtask)
#     )
# except Exception as e:
#     print('Something went wrong: {}'.format(e))
#     dtask.status = DownloadStatus.FAILED
#     dtask.errorMessage = repr(e)
