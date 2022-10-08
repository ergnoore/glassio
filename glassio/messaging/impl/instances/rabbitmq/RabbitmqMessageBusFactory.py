from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping
from typing import Optional

from glassio.logger import ILogger
from glassio.logger import get_initialized_logger
from glassio.mixins import IFactory

from ...message_packer import IPayloadPacker
from ...message_packer import PayloadPackerImpl
from ....core import IMessageTypeMatcher
from ....core import InitializableMessageChannel

from .DefaultMessageTypeMatcher import DefaultMessageTypeMatcher
from .RabbitMessageChannelProperties import RabbitMessageChannelProperties
from .RabbitmqMessageChannel import RabbitmqMessageChannel
from .RabbitmqMessageChannelConfig import RabbitmqMessageChannelConfig


__all__ = [
    "RabbitmqMessageChannelFactory",
]


class RabbitmqMessageChannelFactory(IFactory[InitializableMessageChannel]):

    __slots__ = (
        "__message_packer",
        "__message_type_matcher",
        "__logger",
        "__event_loop",
    )

    def __init__(
        self,
        message_packer: Optional[IPayloadPacker] = None,
        message_type_matcher: Optional[IMessageTypeMatcher[RabbitMessageChannelProperties]] = None,
        logger: Optional[ILogger] = None,
        event_loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        self.__message_packer = message_packer or PayloadPackerImpl()
        self.__message_type_matcher = message_type_matcher or DefaultMessageTypeMatcher()
        self.__logger = logger or get_initialized_logger()
        self.__event_loop = event_loop

    def __call__(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> InitializableMessageChannel:

        settings = settings or {}
        config = RabbitmqMessageChannelConfig(**settings)

        message_channel = RabbitmqMessageChannel(
            config=config,
            message_packer=self.__message_packer,
            message_type_matcher=self.__message_type_matcher,
            logger=self.__logger,
            event_loop=self.__event_loop,
        )

        return message_channel
