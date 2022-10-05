from typing import Optional

from glassio.initializable_components import AbstractInitializableComponent
from glassio.logger import ILogger

from ....core import MessageConsumer
from ....core import IMessageChannel
from ....core import Message


__all__ = [
    "VoidMessageBus",
]


class VoidMessageChannel(IMessageChannel):

    __slots__ = (
        "__logger",
    )

    def __init__(
        self,
        logger: ILogger,
    ) -> None:
        super().__init__()
        self.__logger = logger

    async def publish(
        self,
        message: Message,
    ) -> None:
        await self.__logger.debug(
            "Message published in void: "
            f"message: `{message}`."
        )

    async def add_consumer(self, consumer: MessageConsumer) -> None:
        pass
