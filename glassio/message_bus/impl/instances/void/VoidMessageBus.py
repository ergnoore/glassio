from typing import Optional

from glassio.initializable_components import AbstractInitializableComponent
from glassio.logger import ILogger

from ....core import IConsumer
from ....core import InitializableMessageBus
from ....core import MessageBusException


__all__ = [
    "VoidMessageBus",
]


class VoidMessageBus(InitializableMessageBus, AbstractInitializableComponent):

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
        message: bytes,
        message_type: Optional[str] = None
    ) -> None:
        await self.__logger.debug(
            "MessageBus: "
            "message published in void: "
            f"message: `{message}`, "
            f"message_type: `{message_type}`."
        )

    async def add_consumer(self, consumer: IConsumer) -> None:
        pass
