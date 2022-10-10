from abc import ABC

from typing import Generic
from typing import TypeVar
from typing import Union

from glassio.initializable_components import InitializableComponent

from .EventHandler import EventHandler
from .ISubscription import ISubscription


__all__ = [
    "IEventBus",
]


E = TypeVar('E')


class IEventBus(Generic[E], InitializableComponent, ABC):

    __slots__ = ()

    async def publish(self, event: E) -> None:
        raise NotImplementedError()

    def subscribe(
        self,
        event_alias: Union[Type[E], str],
        event_handler: EventHandler,
    ) -> ISubscription:
        raise NotImplementedError()

    def cancel_subscription(self, subscription: ISubscription) -> None:
        raise NotImplementedError()
