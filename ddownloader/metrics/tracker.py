from ddownloader import config as cfg
from .events import Event
from .trackers.base import EventTracker
from .trackers.central_tracker import CentralEventTracker
from .trackers.otel_tracker import OtelEventTracker


class EventHub:
    __trackers: list[EventTracker] = []

    def _add_tracker(self, tracker: EventTracker) -> None:
        self.__trackers.append(tracker)

    def _remove_tracker(self, tracker: EventTracker) -> None:
        self.__trackers.remove(tracker)

    async def cleanup(self) -> None:
        for tracker in self.__trackers:
            await tracker.cleanup()

    async def on(self, evt: Event, **kwargs) -> None:
        for tracker in self.__trackers:
            await tracker.on(evt, **kwargs)


event_hub = EventHub()


async def cleanup() -> None:
    await event_hub.cleanup()


#################################################
# Initialize main Events hub

if cfg.ct_monitoring_enabled():
    ct_tracker = CentralEventTracker()
    event_hub._add_tracker(ct_tracker)

otel_tracker = OtelEventTracker()
event_hub._add_tracker(otel_tracker)
