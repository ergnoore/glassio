from typing import Collection
from typing import Generic
from typing import TypeVar

from .IEventHandler import IEventHandler


__all__ = [
    "IEventBusConsumer",
]


E = TypeVar('E')


class IEventBusConsumer(Generic[E]):

    """
    Message consumer for Event bus.

    The event can only be consumed or rejected.

    If the handler has successfully worked,
    then the event is considered consumed and will be removed from the bus.

    If the handler raises an exception, the
    event is considered rejected and will not be removed from the bus.
    """

    __slots__ = ()

    async def __call__(
        self,
        event: E,
        handlers: Collection[IEventHandler[E]],
    ) -> None:
        raise NotImplementedError()
