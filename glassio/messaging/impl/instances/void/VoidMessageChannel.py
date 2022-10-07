from glassio.logger import ILogger

from ....core import IMessageChannel
from ....core import Message
from ....core import MessageConsumer


__all__ = [
    "VoidMessageChannel",
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
            f"Message published in void: message: `{message}`."
        )

    async def add_consumer(self, consumer: MessageConsumer) -> None:
        pass
