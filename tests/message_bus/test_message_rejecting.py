import asyncio

import pytest

from .consumers import ToggleConsumer


@pytest.mark.asyncio
async def test_message_rejecting(message_bus_supporting_rejection) -> None:
    """
    The consumer should consume the message only on the second attempt.
    """
    published_message = b"some message."

    consumer = ToggleConsumer()

    await message_bus_supporting_rejection.initialize()
    await message_bus_supporting_rejection.add_consumer(consumer)
    await message_bus_supporting_rejection.publish(published_message)
    await asyncio.sleep(0.1)
    await message_bus_supporting_rejection.deinitialize()

    assert consumer.call_counter == 2
