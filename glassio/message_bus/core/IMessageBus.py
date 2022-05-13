from typing import Optional

from .IConsumer import IConsumer


__all__ = [
    "IMessageBus",
]


class IMessageBus:

    __slots__ = ()

    async def publish(
        self,
        message: bytes,
        message_type: Optional[str] = None,
    ) -> None:
        raise NotImplementedError()

    async def add_consumer(self, consumer: IConsumer) -> None:
        raise NotImplementedError()
