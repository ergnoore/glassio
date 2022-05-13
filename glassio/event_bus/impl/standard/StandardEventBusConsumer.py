from asyncio import AbstractEventLoop
from asyncio import get_event_loop
from asyncio import wait
from typing import Collection
from typing import Optional
from typing import TypeVar

from glassio.logger import ILogger

from ...core import IEventBusConsumer
from ...core import IEventHandler


__all__ = [
    "StandardEventBusConsumer",
]


E = TypeVar('E')


class StandardEventBusConsumer(IEventBusConsumer[E]):

    __slots__ = (
        "__event_loop",
        "__logger",
    )

    def __init__(
        self,
        logger: ILogger,
        event_loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        self.__event_loop = event_loop
        self.__logger = logger

    async def __call_handler(self, handler: IEventHandler[E], event: E) -> None:
        try:
            await handler(event)
        except Exception as e:
            await self.__logger.error(
                f"Error during handler call.",
                exception=e,
            )

    async def __call__(
        self,
        event: E,
        handlers: Collection[IEventHandler[E]],
    ) -> None:

        if self.__event_loop is None:
            self.__event_loop = get_event_loop()

        for handler in handlers:
            self.__event_loop.create_task(
                self.__call_handler(handler, event),
                name="EventHandler."
            )
