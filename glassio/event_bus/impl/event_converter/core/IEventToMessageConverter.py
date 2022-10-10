from typing import Generic
from typing import TypeVar
from typing import Tuple

from glassio.messaging import Message


__all__ = [
    "IEventToMessageConverter",
]


E = TypeVar('E')


class IEventToMessageConverter(Generic[E]):

    __slots__ = ()

    def to_message(self, event_name: str, event: E) -> Message:
        raise NotImplementedError()

    def from_message(self, message: Message) -> Tuple[str, E]:
        raise NotImplementedError()
