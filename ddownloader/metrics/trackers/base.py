from abc import ABC, abstractmethod
from ..events import Event


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

    @abstractmethod
    async def on(self, evt: Event, **kwargs) -> None:
        raise NotImplementedError
