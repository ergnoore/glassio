from typing import Mapping
from typing import Optional
from typing import Type
from typing import TypeVar

from glassio.message_bus import IMessageBus

from ...core import EventDispatchingException
from ...core import IEventDispatcher


__all__ = [
    "StandardEventDispatcher",
]


E = TypeVar('E')


class StandardEventDispatcher(IEventDispatcher[E]):

    __slots__ = (
        "__routes",
        "__default",
    )

    def __init__(
        self,
        routes: Optional[Mapping[Type[E], IMessageBus]] = None,
        default: Optional[IMessageBus] = None,
    ) -> None:
        self.__routes: Mapping[Type[E], IMessageBus] = routes or {}
        self.__default: Optional[IMessageBus] = default

    async def dispatch(self, event: E) -> IMessageBus:
        message_bus = self.__routes.get(type(event), self.__default)

        if message_bus is None:
            raise EventDispatchingException(
                f"An error dispatching the event: `{event}`."
            )

        return message_bus
