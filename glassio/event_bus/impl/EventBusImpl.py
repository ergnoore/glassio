from typing import Optional
from typing import TypeVar

from glassio.initializable_components import InitializedState
from glassio.initializable_components import required_state

from glassio.logger import ILogger

from glassio.messaging import IConsumptionChannel
from glassio.messaging import IPublicationChannel
from glassio.messaging import Message

from .abstract import AbstractEventBus
from .IEventToMessageConverter import IEventToMessageConverter
from ..core import EventBusException
from ..core import EventHandler


__all__ = [
    "EventBusImpl",
]


E = TypeVar('E')


class EventBusImpl(AbstractEventBus[E]):

    __slots__ = (
        "__publication_channel",
        "__consumption_channel",
        "__event_to_message_converter",
        "__reject_if_no_handlers",
        "__logger",
    )

    def __init__(
        self,
        publication_channel: IPublicationChannel,
        consumption_channel: IConsumptionChannel,
        event_to_message_converter: IEventToMessageConverter[E],
        logger: ILogger,
        reject_if_no_handlers: bool = True,
    ) -> None:
        super().__init__()
        self.__publication_channel = publication_channel
        self.__consumption_channel = consumption_channel
        self.__event_to_message_converter = event_to_message_converter
        self.__reject_if_no_handlers = reject_if_no_handlers
        self.__logger = logger

    @required_state(InitializedState)
    async def publish(self, event: E, event_name: Optional[str] = None) -> None:
        event_name = event_name or event.__class__.__name__
        message = self.__event_to_message_converter.to_message(event_name, event)

        await self.__publication_channel.publish(message=message)
        await self.__logger.debug(f"Event published: `{event}`.")

    async def _initialize(self) -> None:
        await self.__consumption_channel.set_consumer(self.__message_consumer)

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        await self.__consumption_channel.pop_consumer()

    async def __call_handler(self, handler: EventHandler, event: E) -> None:
        try:
            await handler(event)
        except Exception as e:
            await self.__logger.error(
                f"Error during handler call.",
                exception=e,
            )

    async def __message_consumer(self, message: Message) -> None:
        try:
            event_name, event = self.__event_to_message_converter.from_message(message)
            if event is None:
                raise TypeError("Event must be object, not None.")
        except Exception as exc:
            raise EventBusException("Error converting a message into an event.") from exc

        handlers = self.__handlers[event_name]

        if len(handlers) and self.__reject_if_no_handlers:
            raise EventBusException("There are no handlers for the event.")

        for handler in handlers:
            self.__event_loop.create_task(
                self.__call_handler(handler, event),
                name="EventHandler."
            )
