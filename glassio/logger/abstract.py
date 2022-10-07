from abc import ABC
from typing import Optional

from glassio.initializable_components import AbstractInitializableComponent

from .core import InitializableLogger
from .core import Level
from .core import Message


__all__ = [
    "AbstractLogger",
]


class AbstractLogger(AbstractInitializableComponent, InitializableLogger, ABC):

    async def debug(self, message: Message) -> None:
        await self.log(Level.DEBUG, message)

    async def info(self, message: Message) -> None:
        await self.log(Level.INFO, message)

    async def warning(self, message: Message, exception: Optional[Exception] = None) -> None:
        await self.log(Level.WARNING, message, exception)

    async def error(self, message: Message, exception: Optional[Exception] = None) -> None:
        await self.log(Level.ERROR, message, exception)

    async def critical(self, message: Message, exception: Optional[Exception] = None) -> None:
        await self.log(Level.CRITICAL, message, exception)
