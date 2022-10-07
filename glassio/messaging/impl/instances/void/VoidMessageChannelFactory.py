from typing import Any
from typing import Mapping
from typing import Optional

from glassio.logger import ILogger
from glassio.mixins import IFactory

from .VoidMessageChannel import VoidMessageChannel

from ....core import IMessageChannel


__all__ = [
    "VoidMessageChannelFactory",
]


class VoidMessageChannelFactory(IFactory[IMessageChannel]):

    __slots__ = (
        "__logger",
    )

    def __init__(
        self,
        logger: ILogger = None,
    ) -> None:
        self.__logger = logger

    def __call__(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> IMessageChannel:
        message_channel = VoidMessageChannel(logger=self.__logger)
        return message_channel
