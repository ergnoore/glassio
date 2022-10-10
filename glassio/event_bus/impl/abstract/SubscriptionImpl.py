from ...core import EventHandler
from ...core import ISubscription


__all__ = [
    "SubscriptionImpl",
]


class SubscriptionImpl(ISubscription):

    __slots__ = (
        "__event_name",
        "__event_handler",
    )

    def __init__(
        self,
        event_name: str,
        event_handler: EventHandler,
    ) -> None:
        self.__event_name = event_name
        self.__event_handler = event_handler

    @property
    def event_name(self) -> str:
        return self.__event_name

    @property
    def event_handler(self) -> EventHandler:
        return self.__event_handler
