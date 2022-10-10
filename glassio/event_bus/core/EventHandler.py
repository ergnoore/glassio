from typing import Any
from typing import Protocol


__all__ = [
    "EventHandler",
]


class EventHandler(Protocol):

    __slots__ = ()

    async def __call__(self, event: Any) -> None:
        raise NotImplementedError()
