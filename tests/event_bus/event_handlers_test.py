import asyncio
from typing import Optional

import pytest

from glassio.event_bus import IEventHandler
from tests.event_bus.events import BaseEvent
from tests.event_bus.events import SimpleEvent


class SimpleHandler(IEventHandler):

    __slots__ = (
        "__handled_event",
    )

    def __init__(self) -> None:
        self.__handled_event: Optional[BaseEvent] = None

    @property
    def handled_event(self) -> Optional[BaseEvent]:
        return self.__handled_event

    async def __call__(self, event: SimpleEvent) -> None:
        self.__handled_event = event


@pytest.mark.asyncio
async def test_handler_call(initialized_event_bus) -> None:
    print(initialized_event_bus)
    handler = SimpleHandler()

    await initialized_event_bus.attach_event_handler(handler)

    event = SimpleEvent(foo="simple event.", bar=123456)
    await initialized_event_bus.publish(event)

    await asyncio.sleep(0.001)

    assert handler.handled_event == event


@pytest.mark.asyncio
async def test_handlers_call(initialized_event_bus) -> None:

    handlers = [SimpleHandler() for _ in range(10)]

    for handler in handlers:
        await initialized_event_bus.attach_event_handler(handler)

    event = SimpleEvent(foo="simple event.", bar=123456)
    await initialized_event_bus.publish(event)

    await asyncio.sleep(0.001)

    for handler in handlers:
        assert handler.handled_event == event


@pytest.mark.asyncio
async def test_detached_handler_call(initialized_event_bus) -> None:

    handler = SimpleHandler()

    await initialized_event_bus.attach_event_handler(handler)
    await initialized_event_bus.detach_event_handler(handler)

    event = SimpleEvent(foo="simple event.", bar=123456)
    await initialized_event_bus.publish(event)

    await asyncio.sleep(0.001)

    assert handler.handled_event is None
