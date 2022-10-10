from abc import ABC

from collections import defaultdict

from typing import MutableMapping
from typing import MutableSequence
from typing import Type
from typing import TypeVar
from typing import Union

from glassio.initializable_components import AbstractInitializableComponent
from .SubscriptionImpl import SubscriptionImpl

from ...core import EventHandler
from ...core import IEventBus
from ...core import ISubscription


__all__ = [
    "AbstractEventBus",
]


E = TypeVar('E')


class AbstractEventBus(IEventBus[E], AbstractInitializableComponent, ABC):

    __slots__ = (
        "_handlers",
    )

    def __init__(self) -> None:
        super().__init__(name="AbstractEventBus")
        self._handlers: MutableMapping[str, MutableSequence[EventHandler]] = defaultdict(list)

    def subscribe(
        self,
        event_alias: Union[Type[E], str],
        event_handler: EventHandler
    ) -> ISubscription:

        event_name = event_alias

        if not isinstance(event_alias, str):
            event_name = event_alias.__name__

        self._handlers[event_alias].append(event_handler)
        return SubscriptionImpl(event_name, event_handler)

    def cancel_subscription(self, subscription: ISubscription) -> None:

        event_name = subscription.event_name

        try:
            self._handlers[event_name].remove(subscription.event_handler)
        except ValueError:
            pass
