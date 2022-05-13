from typing import Generic
from typing import TypeVar


__all__ = [
    "IEventHandler",
]


T = TypeVar('T')


class IEventHandler(Generic[T]):

    """Handler for event."""

    __slots__ = ()

    async def __call__(self, event: T) -> None:
        """Handle the event."""
        raise NotImplementedError()
