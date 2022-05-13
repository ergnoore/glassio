import pytest

from glassio.event_bus import IEventHandler
from glassio.event_bus import HandlerIsNotAttachedException

from tests.event_bus.events import ImportantEvent
from tests.event_bus.events import SimpleEvent


class HandlerWithoutAnnotations(IEventHandler):

    async def __call__(self, foo: str) -> None:
        pass


class HandlerWithAnnotations(IEventHandler):

    async def __call__(self, event: SimpleEvent) -> None:
        pass


@pytest.mark.asyncio
async def test_attach_and_detach_handler(initialized_event_bus):

    handler = HandlerWithAnnotations()

    await initialized_event_bus.attach_event_handler(handler)
    await initialized_event_bus.detach_event_handler(handler)


@pytest.mark.asyncio
async def test_attach_and_double_detach_handler(initialized_event_bus):

    handler = HandlerWithAnnotations()

    await initialized_event_bus.attach_event_handler(handler)
    await initialized_event_bus.detach_event_handler(handler)

    with pytest.raises(HandlerIsNotAttachedException):
        await initialized_event_bus.detach_event_handler(handler)


@pytest.mark.asyncio
async def test_attach_handler_without_annotations(initialized_event_bus):

    handler = HandlerWithoutAnnotations()

    with pytest.raises(AttributeError):
        await initialized_event_bus.attach_event_handler(handler)


@pytest.mark.asyncio
async def test_attach_invalid_handler_with_event_type(initialized_event_bus):

    handler = HandlerWithoutAnnotations()

    await initialized_event_bus.attach_event_handler(handler, event_type=SimpleEvent)
    await initialized_event_bus.detach_event_handler(handler, event_type=SimpleEvent)


@pytest.mark.asyncio
async def test_attach_handler_with_annotations(initialized_event_bus):

    handler = HandlerWithAnnotations()

    await initialized_event_bus.attach_event_handler(handler)


@pytest.mark.asyncio
async def test_attach_handler_with_annotations_and_event_type(initialized_event_bus):

    handler = HandlerWithAnnotations()

    await initialized_event_bus.attach_event_handler(handler, event_type=ImportantEvent)
    await initialized_event_bus.detach_event_handler(handler, event_type=ImportantEvent)
