from typing import Any
from typing import Mapping
from typing import Optional
from typing import TypeVar

from glassio.logger import ILogger
from glassio.logger import get_initialized_logger
from glassio.mixins import IFactory

from .EventBusConfig import EventBusConfig
from .EventBusImpl import EventBusImpl
from .standard import StandardDeserializationExceptionHandler
from .standard import StandardEventBusConsumer
from .standard import StandardEventDispatcher

from ..core import IDeserializationExceptionHandler
from ..core import IEventBusConsumer
from ..core import IEventDispatcher
from ..core import IEventSerializer
from ..core import InitializableEventBus


__all__ = [
    "EventBusFactory",
]


E = TypeVar('E')


class EventBusFactory(IFactory[InitializableEventBus[E]]):

    def __init__(
        self,
        event_serializer: IEventSerializer[E],
        logger: Optional[ILogger] = None,
        event_dispatcher: Optional[IEventDispatcher[E]] = None,
        deserialization_exception_handler: Optional[IDeserializationExceptionHandler] = None,
        consumer: Optional[IEventBusConsumer[E]] = None,
    ) -> None:
        self.__event_serializer = event_serializer
        self.__logger = logger or get_initialized_logger()
        self.__event_dispatcher = event_dispatcher or StandardEventDispatcher()
        self.__consumer = consumer or StandardEventBusConsumer(logger=logger)
        self.__deserialization_exception_handler = deserialization_exception_handler or \
            StandardDeserializationExceptionHandler(logger)

    def __call__(self, settings: Optional[Mapping[str, Any]] = None) -> InitializableEventBus:

        settings = settings or {}
        config = EventBusConfig(**settings)

        return EventBusImpl(
            config=config,
            event_dispatcher=self.__event_dispatcher,
            event_serializer=self.__event_serializer,
            consumer=self.__consumer,
            deserialization_exception_handler=self.__deserialization_exception_handler,
            logger=self.__logger,
        )
