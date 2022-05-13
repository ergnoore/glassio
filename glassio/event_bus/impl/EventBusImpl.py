from typing import Optional
from typing import TypeVar

from glassio.logger import ILogger

from .abstract import AbstractInitializableEventBus
from .EventBusConfig import EventBusConfig

from ..core import IDeserializationExceptionHandler
from ..core import IEventBusConsumer
from ..core import IEventDispatcher
from ..core import IEventSerializer


__all__ = [
    "EventBusImpl",
]


E = TypeVar('E')


class EventBusImpl(AbstractInitializableEventBus[E]):

    __slots__ = (
        "__config",
        "__event_dispatcher",
        "__event_serializer",
        "__consumer",
        "__deserialization_exception_handler",
        "__logger",
    )

    def __init__(
        self,
        config: EventBusConfig,
        event_dispatcher: IEventDispatcher[E],
        event_serializer: IEventSerializer[E],
        consumer: IEventBusConsumer[E],
        deserialization_exception_handler: IDeserializationExceptionHandler,
        logger: ILogger,
    ) -> None:
        super().__init__()
        self.__config = config
        self.__event_dispatcher = event_dispatcher
        self.__event_serializer = event_serializer
        self.__consumer = consumer
        self.__deserialization_exception_handler = deserialization_exception_handler
        self.__logger = logger

    async def publish(self, event: E) -> None:
        target_message_bus = await self.__event_dispatcher.dispatch(event)
        message, message_type = self.__event_serializer.serialize(event)

        await target_message_bus.publish(
            message=message,
            message_type=message_type,
        )
        await self.__logger.debug(
            f"EventBus: publish event: `{event}` "
            f"in message_bus: `{target_message_bus}`."
        )

    async def __consumer_wrapper(self, message: bytes, message_type: Optional[str]) -> None:
        try:
            event = self.__event_serializer.deserialize(message, message_type)
            if event is None:
                raise TypeError(
                    "Event must be object, not None."
                )
        except Exception as exc:
            await self.__deserialization_exception_handler(message, message_type, exc)
            return

        handlers = self._get_handlers(event_type=type(event))
        try:
            await self.__consumer(event, handlers)
        except Exception as exc:
            await self.__logger.error(
                "Error during operation of the event consumer.",
                exception=exc,
            )
            raise exc

    async def _initialize(self) -> None:
        for message_bus, number_of_consumers in self.__config.number_of_consumers.items():
            for _ in range(number_of_consumers):
                await message_bus.add_consumer(self.__consumer_wrapper)
