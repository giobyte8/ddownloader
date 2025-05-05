from abc import ABC, abstractmethod
from ddownloader.models import HttpGallerySource
from enum import StrEnum


class Event(StrEnum):
    SRC_DL_START = "src_dl_start"
    SRC_DL_END   = "src_dl_end"


class EventTracker(ABC):
    """
    Base class for event trackers.
    """

    def __init__(self, name: str = "default"):
        self.name = name

    @abstractmethod
    async def cleanup(self) -> None:
        raise NotImplementedError(
            "cleanup must be implemented in subclasses"
        )

    async def on(self, evt: Event, **kwargs) -> None:
        if evt == Event.SRC_DL_START:
            await self.on_src_dl_start(**kwargs)
        elif evt == Event.SRC_DL_END:
            await self.on_src_dl_end(**kwargs)

    @abstractmethod
    async def on_src_dl_start(self, src: HttpGallerySource) -> None:
        raise NotImplementedError(
            "on_src_dl_start must be implemented in subclasses"
        )

    @abstractmethod
    async def on_src_dl_end(self, src: HttpGallerySource) -> None:
        raise NotImplementedError(
            "on_src_dl_end must be implemented in subclasses"
        )
