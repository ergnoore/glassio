from typing import Optional

from glassio.message_bus import IConsumer


__all__ = [
    "SimpleConsumer",
]


class SimpleConsumer(IConsumer):

    __slots__ = (
        "_call_counter",
        "_consumed_message",
        "_message_type",
    )

    def __init__(self) -> None:
        self._call_counter: int = 0
        self._consumed_message: Optional[bytes] = None
        self._message_type: Optional[str] = None

    @property
    def call_counter(self) -> int:
        return self._call_counter

    @property
    def consumed_message(self) -> bytes:
        return self._consumed_message

    @property
    def consumed_message_type(self) -> Optional[str]:
        return self._message_type

    async def __call__(self, message: bytes, message_type: Optional[str]) -> None:
        self._call_counter += 1
        self._consumed_message = message
        self._message_type = message_type
