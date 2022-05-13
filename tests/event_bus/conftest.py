import pytest
import pytest_asyncio

from glassio.event_bus import EventBusFactory
from glassio.event_bus import IEventBus
from glassio.event_bus import IEventBusConsumer
from glassio.event_bus import IEventDispatcher
from glassio.event_bus import IEventSerializer
from glassio.event_bus import InitializableEventBus
from glassio.event_bus import StandardEventBusConsumer
from glassio.event_bus import StandardEventDispatcher

from .events import BaseEvent
from .events import EventSerializer


@pytest_asyncio.fixture()
async def initialized_event_bus_without_dispatching(initialized_logger) -> InitializableEventBus:

    event_serializer: IEventSerializer[BaseEvent] = EventSerializer()

    event_dispatcher: IEventDispatcher[BaseEvent] = StandardEventDispatcher()
    event_consumer: IEventBusConsumer[BaseEvent] = StandardEventBusConsumer(
        logger=initialized_logger,
    )

    event_bus_factory = EventBusFactory(
        event_dispatcher=event_dispatcher,
        event_serializer=event_serializer,
        consumer=event_consumer,
        logger=initialized_logger,
    )

    event_bus = event_bus_factory.get_instance()
    await event_bus.initialize()
    yield event_bus
    await event_bus.deinitialize()


@pytest.fixture()
def event_bus(initialized_message_bus, initialized_logger) -> InitializableEventBus:

    event_serializer: IEventSerializer[BaseEvent] = EventSerializer()

    event_dispatcher: IEventDispatcher[BaseEvent] = StandardEventDispatcher(default=initialized_message_bus)
    event_consumer: IEventBusConsumer[BaseEvent] = StandardEventBusConsumer(
        logger=initialized_logger,
    )

    event_bus_factory = EventBusFactory(
        event_dispatcher=event_dispatcher,
        event_serializer=event_serializer,
        consumer=event_consumer,
        # logger=initialized_logger,
    )

    return event_bus_factory.get_instance(
        settings={
            "number_of_consumers": {
                initialized_message_bus: 1,
            }
        }
    )


@pytest_asyncio.fixture()
async def initialized_event_bus(event_bus) -> IEventBus:
    await event_bus.initialize()
    yield event_bus
    await event_bus.deinitialize()
