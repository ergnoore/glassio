from abc import ABC
from collections import defaultdict
from typing import Collection
from typing import MutableMapping
from typing import MutableSequence
from typing import Optional
from typing import Type
from typing import TypeVar

from glassio.initializable_components import AbstractInitializableComponent

from ..get_event_type_from_annotations import get_event_type_from_annotations
from ...core import HandlerIsNotAttachedException
from ...core import IEventHandler
from ...core import InitializableEventBus


__all__ = [
    "AbstractInitializableEventBus",
]


E = TypeVar('E')


class AbstractInitializableEventBus(AbstractInitializableComponent, InitializableEventBus[E], ABC):

    __slots__ = (
        "_handlers",
    )

    def __init__(self) -> None:
        super().__init__()
        self._handlers: MutableMapping[Type[E], MutableSequence[IEventHandler[E]]] = defaultdict(list)

    async def attach_event_handler(
        self,
        event_handler: IEventHandler[E],
        event_type: Optional[E] = None,
    ) -> None:
        event_type = event_type or get_event_type_from_annotations(event_handler)
        self._handlers[event_type].append(event_handler)

    async def detach_event_handler(
        self,
        event_handler: IEventHandler[E],
        event_type: Optional[E] = None,
    ) -> None:
        event_type = event_type or get_event_type_from_annotations(event_handler)
        try:
            self._handlers[event_type].remove(event_handler)
        except ValueError:
            raise HandlerIsNotAttachedException(event_handler)

    def _get_handlers(self, event_type: Type[E]) -> Collection[IEventHandler[E]]:
        return self._handlers[event_type]
