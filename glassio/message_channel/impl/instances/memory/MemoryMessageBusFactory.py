from asyncio import AbstractEventLoop
from asyncio import PriorityQueue
from typing import Any
from typing import Mapping
from typing import Optional

from glassio.logger import get_initialized_logger
from glassio.logger import ILogger
from glassio.mixins import IFactory

from .DefaultMessageTypeMatcher import DefaultMessageTypeMatcher
from .MemoryMessageBus import MemoryMessageBus
from .MemoryMessageBusProperties import MemoryMessageBusProperties

from ....core import IMessageTypeMatcher
from ....core import InitializableMessageBus


__all__ = [
    "MemoryMessageBusFactory",
]


class MemoryMessageBusFactory(IFactory[InitializableMessageBus]):

    __slots__ = (
        "__message_type_matcher",
        "__priority_queue",
        "__logger",
        "__event_loop",
    )

    def __init__(
        self,
        message_type_matcher: Optional[IMessageTypeMatcher[MemoryMessageBusProperties]] = None,
        priority_queue: Optional[PriorityQueue] = None,
        logger: Optional[ILogger] = None,
        event_loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        self.__message_type_matcher = message_type_matcher or DefaultMessageTypeMatcher()
        self.__priority_queue = priority_queue or PriorityQueue()
        self.__logger = logger or get_initialized_logger()
        self.__event_loop = event_loop

    def __call__(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> InitializableMessageBus:

        return MemoryMessageBus(
            queue=self.__priority_queue,
            message_type_matcher=self.__message_type_matcher,
            event_loop=self.__event_loop,
            logger=self.__logger,
        )
