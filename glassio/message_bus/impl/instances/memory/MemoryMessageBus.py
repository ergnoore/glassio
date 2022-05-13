from asyncio import AbstractEventLoop
from asyncio import CancelledError
from asyncio import Future
from asyncio import PriorityQueue
from asyncio import Task
from asyncio import get_event_loop

from itertools import cycle
from time import time
from typing import Any
from typing import Iterator
from typing import MutableSequence
from typing import Optional
from typing import Tuple

from glassio.initializable_components import AbstractInitializableComponent
from glassio.initializable_components import InitializedState
from glassio.initializable_components import required_state
from glassio.logger import ILogger

from ....core import IConsumer
from ....core import IMessageTypeMatcher
from ....core import InitializableMessageBus

from .MemoryMessageBusProperties import MemoryMessageBusProperties
from .MessageWrapper import MessageWrapper


__all__ = [
    "MemoryMessageBus",
]


class MemoryMessageBus(InitializableMessageBus, AbstractInitializableComponent):

    __slots__ = (
        "__queue",
        "__message_type_matcher",
        "__event_loop",
        "__consumers",
        "__consumer_iterator",
        "__background_task",
        "__consumer_added",
        "__logger",
    )

    def __init__(
        self,
        queue: PriorityQueue,
        message_type_matcher: IMessageTypeMatcher[MemoryMessageBusProperties],
        logger: ILogger,
        event_loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        super().__init__()
        self.__queue = queue
        self.__message_type_matcher = message_type_matcher
        self.__event_loop = event_loop

        self.__consumers: MutableSequence[IConsumer] = []
        self.__consumer_iterator: Iterator[IConsumer] = cycle(self.__consumers)
        self.__background_task: Optional[Task] = None
        self.__consumer_added: Future[Any] = Future()
        self.__logger = logger

    async def _initialize(self) -> None:
        if self.__event_loop is None:
            self.__event_loop = get_event_loop()

        self.__background_task = self.__event_loop.create_task(
            self.__publishing_task(),
            name="MemoryMessageBus publishing task."
        )

    async def _deinitialize(
        self,
        exception: Optional[Exception] = None
    ) -> None:
        if self.__background_task is not None:
            self.__background_task.cancel()

    async def __put_message(
        self,
        message: bytes,
        message_type: Optional[str],
    ) -> None:
        properties = self.__message_type_matcher.match(message_type)
        message_wrapper = MessageWrapper(
            message=message,
            message_type=message_type,
            properties=properties,
        )
        await self.__queue.put(message_wrapper)

    @required_state(InitializedState)
    async def publish(
        self,
        message: bytes,
        message_type: Optional[str] = None
    ) -> None:
        await self.__put_message(message, message_type)
        await self.__logger.debug(
            "MessageBus: "
            "message published: "
            f"message: `{message}`, "
            f"message_type: `{message_type}`."
        )

    @required_state(InitializedState)
    async def add_consumer(self, consumer: IConsumer) -> None:
        self.__consumers.append(consumer)
        # Set the future for `__get_consumer` method.
        if not self.__consumer_added.done():
            self.__consumer_added.set_result(True)

    async def __publish(
        self,
        consumer: IConsumer,
        message: bytes,
        message_type: Optional[str],
    ) -> None:
        async def confirming_wrapper() -> None:
            try:
                await consumer(message, message_type)
            except Exception as e:
                await self.__logger.warning(
                    "MessageBus: "
                    "message consumption error "
                    f"message: `{message}`, "
                    f"message_type: `{message_type}`.",
                    exception=e,
                )
                # republish message
                await self.__put_message(
                    message=message,
                    message_type=message_type,
                )
            else:
                await self.__logger.debug(
                    "MessageBus: "
                    "message consumed "
                    f"message: `{message}`, "
                    f"message_type: `{message_type}`."
                )

        self.__event_loop.create_task(
            confirming_wrapper(),
            name=f"MemoryMessageBus consumer: `{consumer}`."
        )

    async def __get_consumer(self) -> IConsumer:
        # Waiting for at least one consumer to be added.
        await self.__consumer_added
        return next(self.__consumer_iterator)

    async def __get_message(self) -> Tuple[bytes, Optional[str]]:
        message_wrapper = await self.__queue.get()
        time_now = time()
        return message_wrapper.unwrap(time_now)

    async def __publishing_task(self) -> None:
        try:
            while True:
                try:
                    message, message_type = await self.__get_message()
                except TimeoutError as e:
                    await self.__logger.debug(
                        f"MessageBus: {e}"
                    )
                    continue
                consumer = await self.__get_consumer()
                await self.__publish(consumer, message, message_type)
        except CancelledError:
            pass
