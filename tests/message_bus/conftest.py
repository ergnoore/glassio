from typing import Literal

import pytest
import pytest_asyncio

from glassio.message_bus import InitializableMessageBus
from glassio.message_bus import MemoryMessageBusFactory
from glassio.message_bus import RabbitmqMessageBusFactory


def get_message_bus_by_name(name: Literal["rabbitmq", "memory"]) -> InitializableMessageBus:
    if name == "rabbitmq":
        factory = RabbitmqMessageBusFactory()
        return factory.get_instance(
            {
                "settings_for_publishing":
                {
                    "exchange_name": "test_exchange",
                    "routing_key": "test_message_bus",
                    "queue_name": "test_message_bus"
                },
                "settings_for_consuming": {
                    "queue_name": "test_message_bus",
                }
            }
        )

    if name == "memory":
        factory = MemoryMessageBusFactory()
        return factory.get_instance()

    raise Exception("Unknown bus name.")


@pytest.fixture(params=["memory", "rabbitmq"])
def message_bus(
    request,
) -> InitializableMessageBus:
    return get_message_bus_by_name(request.param)


@pytest_asyncio.fixture
async def initialized_message_bus(message_bus):
    await message_bus.initialize()
    yield message_bus
    await message_bus.deinitialize()


@pytest.fixture(params=["memory", "rabbitmq"])
def message_bus_supporting_rejection(request) -> InitializableMessageBus:
    return get_message_bus_by_name(request.param)
