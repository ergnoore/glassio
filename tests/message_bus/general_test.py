import asyncio

import pytest

from .consumers import SimpleConsumer


@pytest.mark.asyncio
async def test_consumer_call(initialized_message_bus) -> None:
    """
    The consumer must receive the message and be called once.
    """

    published_message = b"some message."

    consumer = SimpleConsumer()

    await initialized_message_bus.add_consumer(consumer)
    await initialized_message_bus.publish(published_message)
    await asyncio.sleep(0.001)

    assert consumer.call_counter == 1
    assert consumer.consumed_message == published_message


@pytest.mark.asyncio
async def test_of_calling_multiple_consumers(initialized_message_bus) -> None:
    """
    The number of messages published must be equal to the
    number of messages consumed.

    Each consumer must be called at least once.
    """

    number_of_publications = 20
    published_message = b"some message."

    consumers = [SimpleConsumer() for _ in range(10)]

    for consumer in consumers:
        await initialized_message_bus.add_consumer(consumer)

    for _ in range(number_of_publications):
        await initialized_message_bus.publish(published_message)

    await asyncio.sleep(0.01)

    total_calls = sum([consumers.call_counter for consumers in consumers])

    assert total_calls == number_of_publications

    for consumer in consumers:
        assert consumer.call_counter < 20
        assert consumer.call_counter > 0
