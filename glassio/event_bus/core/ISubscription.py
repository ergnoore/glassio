from .EventHandler import EventHandler


__all__ = [
    "ISubscription",
]


class ISubscription:

    __slots__ = ()

    @property
    def event_name(self) -> str:
        raise NotImplementedError()

    @property
    def event_handler(self) -> EventHandler:
        raise NotImplementedError()
