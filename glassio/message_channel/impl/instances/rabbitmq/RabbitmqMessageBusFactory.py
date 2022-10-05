from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping
from typing import Optional

from glassio.logger import ILogger
from glassio.logger import get_initialized_logger
from glassio.mixins import IFactory

from ...payload_packer import IPayloadPacker
from ...payload_packer import PayloadPackerImpl
from ....core import IMessageTypeMatcher
from ....core import InitializableMessageBus

from .DefaultMessageTypeMatcher import DefaultMessageTypeMatcher
from .RabbitMessageBusProperties import RabbitMessageBusProperties
from .RabbitmqMessageBus import RabbitmqMessageBus
from .RabbitmqMessageBusConfig import RabbitmqMessageBusConfig


__all__ = [
    "RabbitmqMessageBusFactory",
]


class RabbitmqMessageBusFactory(IFactory[InitializableMessageBus]):

    __slots__ = (
        "__payload_packer",
        "__message_type_matcher",
        "__logger",
        "__event_loop",
    )

    def __init__(
        self,
        payload_packer: Optional[IPayloadPacker] = None,
        message_type_matcher: Optional[IMessageTypeMatcher[RabbitMessageBusProperties]] = None,
        logger: Optional[ILogger] = None,
        event_loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        self.__payload_packer = payload_packer or PayloadPackerImpl()
        self.__message_type_matcher = message_type_matcher or DefaultMessageTypeMatcher()
        self.__logger = logger or get_initialized_logger()
        self.__event_loop = event_loop

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> InitializableMessageBus:

        settings = settings or {}
        config = RabbitmqMessageBusConfig(**settings)

        message_bus = RabbitmqMessageBus(
            config=config,
            payload_packer=self.__payload_packer,
            message_type_matcher=self.__message_type_matcher,
            logger=self.__logger,
            event_loop=self.__event_loop,
        )

        return message_bus
