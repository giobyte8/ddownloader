
from ddownloader.downloader import DownloadStatus


class InvalidStatusTransitionError(Exception):
    
    def __init__(
        self,
        source_status: DownloadStatus,
        target_status: DownloadStatus
    ) -> None:
        Exception.__init__(self)
        self.message = "Download task can not change its status from {} to {}".format(
            source_status.value,
            target_status.value
        )
