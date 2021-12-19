from pathlib import PurePath

import ddownloader.dtask_repository as dtask_repo
from ddownloader import async_tasks
from ddownloader.config_loader import downloads_dir
from ddownloader.downloader import DownloadStatus, DownloadTask
from ddownloader.errors import InvalidStatusTransitionError
from ddownloader.web.models import DownloadTasksPage


def create_and_queue(
    url: str,
    relative_target_path: str,
    file_hash: str
) -> DownloadTask:
    """Creates a new download tasks with given arguments
    and queue it for being processed in background.

    Args:
        url (str): Download target
        relative_target_path (str): Local file name for downloaded
            file
        file_hash (str): If provided, hash will be verified against
            downloaded file when download is complete

    Returns:
        DownloadTask: Created task
    """
    target_path = PurePath(
        downloads_dir(),
        relative_target_path
    )

    dtask = DownloadTask(
        url=url,
        target_path=str(target_path),
        file_hash=file_hash
    )
    dtask_repo.save(dtask)

    # Enqueue to download in background
    async_tasks.download(dtask.id)

    return dtask


def get_page(page: int, page_size: int) -> DownloadTasksPage:
    dtasks = dtask_repo.paginate(page_size, page)
    count = dtask_repo.count()

    return DownloadTasksPage(
        page,
        page_size,
        count,
        dtasks
    )

def update_status(dtask_id: int, to_status: DownloadStatus) -> DownloadTask:
    dtask = dtask_repo.find_by_id(dtask_id)
    
    if dtask.status in [DownloadStatus.QUEUED, DownloadStatus.IN_PROGRESS]:
        if to_status != DownloadStatus.PAUSED:
            raise InvalidStatusTransitionError(dtask.status, to_status)
    
    elif dtask.status in [DownloadStatus.PAUSED, DownloadStatus.FAILED]:
        if to_status != DownloadStatus.QUEUED:
            raise InvalidStatusTransitionError(dtask.status, to_status)

    
    # Exception was not raised, update dtask
    dtask.status = to_status
    dtask_repo.save(dtask)
    return dtask

def remove(task_id: int) -> None:
    dtask_repo.delete_by_id(task_id)
