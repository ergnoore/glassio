from io import StringIO
import logging

import pytest

from glassio.logger import Level
from glassio.logger import StandardLoggerFactory


@pytest.mark.asyncio
async def test_log() -> None:
    stream = StringIO()

    root_logger = logging.getLogger("Test")

    root_logger.setLevel(logging.DEBUG)
    root_handler = logging.StreamHandler(stream)
    root_handler.setFormatter(
        logging.Formatter("%(levelname)s %(name)s: %(message)s")
    )
    root_logger.addHandler(root_handler)

    logger_factory = StandardLoggerFactory()
    logger = logger_factory("Test")

    await logger.initialize()
    await logger.log(Level.INFO, "Message.")
    await logger.deinitialize()

    assert "INFO Test: Message." in stream.getvalue()


@pytest.mark.asyncio
async def test_log_with_synchronous_factory() -> None:
    stream = StringIO()

    root_logger = logging.getLogger("Test")

    root_logger.setLevel(logging.DEBUG)
    root_handler = logging.StreamHandler(stream)
    root_handler.setFormatter(
        logging.Formatter("%(levelname)s %(name)s: %(message)s")
    )
    root_logger.addHandler(root_handler)

    logger_factory = StandardLoggerFactory()
    logger = logger_factory("Test")

    await logger.initialize()

    def get_message() -> str:
        return "I was returned from a function."

    await logger.log(Level.INFO, get_message)
    await logger.deinitialize()

    assert "INFO Test: I was returned from a function." in stream.getvalue()


@pytest.mark.asyncio
async def test_log_with_coroutine_factory() -> None:
    stream = StringIO()

    root_logger = logging.getLogger("Test")

    root_logger.setLevel(logging.DEBUG)
    root_handler = logging.StreamHandler(stream)
    root_handler.setFormatter(
        logging.Formatter("%(levelname)s %(name)s: %(message)s")
    )
    root_logger.addHandler(root_handler)

    logger_factory = StandardLoggerFactory()
    logger = logger_factory("Test")

    await logger.initialize()

    async def get_message() -> str:
        return "I was returned from a coroutine."

    await logger.log(Level.INFO, get_message())
    await logger.deinitialize()

    assert "INFO Test: I was returned from a coroutine." in stream.getvalue()


@pytest.mark.asyncio
async def test_log_with_exception() -> None:
    stream = StringIO()

    root_logger = logging.getLogger("Test")

    root_logger.setLevel(logging.DEBUG)
    root_handler = logging.StreamHandler(stream)
    root_handler.setFormatter(
        logging.Formatter("%(levelname)s %(name)s: %(message)s")
    )
    root_logger.addHandler(root_handler)

    logger_factory = StandardLoggerFactory()
    logger = logger_factory("Test")

    await logger.initialize()

    await logger.log(
        Level.ERROR,
        "Some error.",
        exception=ArithmeticError("Return to school.")
    )
    await logger.deinitialize()

    assert "ERROR Test: Some error." in stream.getvalue()
    assert "ArithmeticError: Return to school." in stream.getvalue()
