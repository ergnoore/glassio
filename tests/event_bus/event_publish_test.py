import pytest

from glassio.event_bus import EventDispatchingException
from glassio.event_bus import EventSerializationException

from tests.event_bus.events import SimpleEvent
from tests.event_bus.events import UnserializableEvent


@pytest.mark.asyncio
async def test_publish_event(initialized_event_bus):
    event = SimpleEvent(foo="foo", bar=1)
    await initialized_event_bus.publish(event)


@pytest.mark.asyncio
async def test_publish_unserializable_event(initialized_event_bus):
    event = UnserializableEvent()

    with pytest.raises(EventSerializationException):
        await initialized_event_bus.publish(event)


@pytest.mark.asyncio
async def test_publish_undispatchible_event(initialized_event_bus_without_dispatching):
    event = SimpleEvent(foo="foo", bar=1)

    with pytest.raises(EventDispatchingException):
        await initialized_event_bus_without_dispatching.publish(event)
