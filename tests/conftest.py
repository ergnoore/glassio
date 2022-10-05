import logging

import pytest
import pytest_asyncio

from glassio.dispatcher import IDispatcher
from glassio.dispatcher import LocalDispatcher
from glassio.logger import ILogger
from glassio.logger import StandardLogger
from glassio.logger import StandardLoggerFactory
from glassio.logger import get_initialized_logger
from glassio.message_channel import IMessageBus
from glassio.message_channel import MemoryMessageBusFactory


@pytest_asyncio.fixture
async def initialized_logger() -> ILogger:
    logging.basicConfig()
    logger_factory = StandardLoggerFactory()
    logger = logger_factory(name="TestLogger")
    await logger.initialize()
    yield logger
    await logger.deinitialize()


@pytest_asyncio.fixture
async def initialized_message_bus(initialized_logger) -> IMessageBus:
    message_bus_factory = MemoryMessageBusFactory(logger=initialized_logger)
    message_bus = message_bus_factory.get_instance()
    await message_bus.initialize()
    yield message_bus
    await message_bus.deinitialize()


@pytest.fixture()
def dispatcher(initialized_logger) -> IDispatcher:
    return LocalDispatcher(initialized_logger)
