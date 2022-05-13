from abc import ABC
from typing import Optional

from glassio.initializable_components import AbstractInitializableComponent
from glassio.initializable_components import InitializedState
from glassio.initializable_components import required_state

from .core import InitializableLogger
from .core import Level
from .core import Message


__all__ = [
    "AbstractLogger",
]


class AbstractLogger(AbstractInitializableComponent, InitializableLogger, ABC):

    @required_state(InitializedState)
    async def debug(self, message: Message) -> None:
        await self.log(Level.DEBUG, message)

    @required_state(InitializedState)
    async def info(self, message: Message) -> None:
        await self.log(Level.INFO, message)

    @required_state(InitializedState)
    async def warning(self, message: Message, exception: Optional[Exception] = None) -> None:
        await self.log(Level.WARNING, message, exception)

    @required_state(InitializedState)
    async def error(self, message: Message, exception: Optional[Exception] = None) -> None:
        await self.log(Level.ERROR, message, exception)

    @required_state(InitializedState)
    async def critical(self, message: Message, exception: Optional[Exception] = None) -> None:
        await self.log(Level.CRITICAL, message, exception)
