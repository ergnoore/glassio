from typing import Generic
from typing import Optional
from typing import TypeVar

from .IEventHandler import IEventHandler


__all__ = [
    "IEventBus",
]


E = TypeVar('E')


class IEventBus(Generic[E]):

    """Event Bus."""

    __slots__ = ()

    async def publish(self, event: E) -> None:
        """Publish an event."""
        raise NotImplementedError()

    async def attach_event_handler(
        self,
        event_handler: IEventHandler[E],
        event_type: Optional[E] = None,
    ) -> None:
        """
        :raise AttributeError: If handler missing event annotation.
        """
        raise NotImplementedError()

    async def detach_event_handler(
        self,
        event_handler: IEventHandler[E],
        event_type: Optional[E] = None,
    ) -> None:
        """
        :raise AttributeError: If handler missing event annotation.
        :raise HandlerIsNotAttachedException:
        """
        raise NotImplementedError()
