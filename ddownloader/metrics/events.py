from enum import StrEnum


_SRC_DOWNLOAD_PREFIX = 'src.download'


class Event(StrEnum):
    pass


class SrcDownloadEvent(Event):
    START = f"{ _SRC_DOWNLOAD_PREFIX }.start"
    END   = f"{ _SRC_DOWNLOAD_PREFIX }.end"
    FILE_DOWNLOADED = f"{ _SRC_DOWNLOAD_PREFIX }.file.downloaded"
    FILE_SKIPPED    = f"{ _SRC_DOWNLOAD_PREFIX }.file.skipped"