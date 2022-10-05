from typing import Any
from typing import Mapping
from typing import Optional

from glassio.logger import get_initialized_logger
from glassio.logger import ILogger
from glassio.mixins import IFactory

from .VoidMessageBus import VoidMessageBus
from ....core import InitializableMessageBus


__all__ = [
    "VoidMessageBusFactory",
]


class VoidMessageBusFactory(IFactory[InitializableMessageBus]):

    __slots__ = (
        "__logger",
    )

    def __init__(
        self,
        logger: Optional[ILogger] = None,
    ) -> None:
        self.__logger = logger or get_initialized_logger()

    def __call__(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> InitializableMessageBus:

        message_bus = VoidMessageBus(
            logger=self.__logger,
        )

        return message_bus
