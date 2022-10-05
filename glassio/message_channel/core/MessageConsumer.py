from typing import Protocol

from .Message import Message


__all__ = [
    "MessageConsumer",
]


class MessageConsumer(Protocol):

    __slots__ = ()

    async def __call__(self, message: Message) -> None:
        raise NotImplementedError()
