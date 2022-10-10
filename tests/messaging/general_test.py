import asyncio

import pytest

from .consumers import SimpleConsumer
from glassio.messaging import Message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message",
    [
        Message({}, b"message"),
        Message({"foo": "bar", "baz": 123}, b"message"),
        Message({}, b"message" * 1024)
    ]
)
async def test_channel(message_channel, message) -> None:
    message_consumer_was_called = False

    async def message_consumer(consumed_message: Message) -> None:
        nonlocal message_consumer_was_called, message
        message_consumer_was_called = True

        assert message.headers == consumed_message.headers
        assert message.body == consumed_message.body

    await message_channel.set_consumer(message_consumer)
    await message_channel.publish(message)

    assert message_consumer_was_called
