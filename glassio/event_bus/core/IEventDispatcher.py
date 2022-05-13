from typing import Generic
from typing import TypeVar

from glassio.message_bus import IMessageBus


__all__ = [
    "IEventDispatcher",
]


E = TypeVar('E')


class IEventDispatcher(Generic[E]):
    """
    Event Dispatcher.

    Dispatch an event to the target message bus.
    """

    __slots__ = ()

    async def dispatch(self, event: E) -> IMessageBus:
        """
        Returns the target message bus for the event.

        :param event: Dispatchable event.
        :return: Target message bus.
        """
        raise NotImplementedError()
