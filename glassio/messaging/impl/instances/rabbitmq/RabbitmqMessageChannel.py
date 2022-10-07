from asyncio import AbstractEventLoop
from asyncio import BaseTransport
from asyncio import Lock
from asyncio import get_event_loop
from typing import Optional

from aioamqp import connect
from aioamqp.channel import Channel
from aioamqp.envelope import Envelope
from aioamqp.properties import Properties
from aioamqp.protocol import AmqpProtocol

from glassio.initializable_components import AbstractInitializableComponent
from glassio.initializable_components import InitializedState
from glassio.initializable_components import required_state
from glassio.logger import ILogger

from .RabbitMessageChannelProperties import RabbitMessageChannelProperties
from .RabbitmqMessageChannelConfig import RabbitmqMessageChannelConfig
from ...message_packer import IPayloadPacker

from ....core import MessageConsumer
from ....core import IMessageTypeMatcher
from ....core import InitializableMessageChannel
from ....core import MessageChannelException
from ....core import PublicationException


__all__ = [
    "RabbitmqMessageChannel",
]


class RabbitmqMessageChannel(AbstractInitializableComponent, InitializableMessageChannel):

    __slots__ = (
        "__config",
        "__payload_packer",
        "__message_type_matcher",
        "__event_loop",
        "__logger",
        "__lock",
        "__transport",
        "__protocol",
        "__channel",
    )

    def __init__(
        self,
        config: RabbitmqMessageChannelConfig,
        payload_packer: IPayloadPacker,
        message_type_matcher: IMessageTypeMatcher[RabbitMessageChannelProperties],
        logger: ILogger,
        event_loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        super().__init__()
        self.__config = config
        self.__payload_packer = payload_packer
        self.__message_type_matcher = message_type_matcher
        self.__logger = logger
        self.__event_loop = event_loop

        self.__lock: Lock = Lock()
        self.__transport: Optional[BaseTransport] = None
        self.__protocol: Optional[AmqpProtocol] = None
        self.__channel: Optional[Channel] = None

    async def __connect(self) -> None:
        async with self.__lock:
            try:
                self.__transport, self.__protocol = await connect(
                    **self.__config.rabbitmq.dict(),
                    loop=self.__event_loop,
                )
                self.__channel: Channel = await self.__protocol.channel()
            except Exception as e:
                raise Exception(
                    f"Fail to connect to {self.__config.rabbitmq.host}. {e!r}."
                )

    async def _initialize(self) -> None:
        if self.__event_loop is None:
            self.__event_loop = get_event_loop()

        await self.__connect()

        if self.__config.settings_for_publishing is None:
            return

    async def __disconnect(self) -> None:
        if self.__protocol is not None:
            await self.__protocol.close()
        if self.__transport is not None:
            self.__transport.close()

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        await self.__disconnect()

    @required_state(InitializedState)
    async def publish(
        self,
        message: bytes,
        message_type: Optional[str] = None,
    ) -> None:

        properties = self.__message_type_matcher.match(message_type)
        payload = self.__payload_packer.pack_payload(message, message_type)

        if self.__config.settings_for_publishing is None:
            raise MessageChannelException(
                "To publish a message, you need to specify the `exchange_name`."
            )

        try:
            await self.__channel.basic_publish(
                payload=payload,
                exchange_name=self.__config.settings_for_publishing.exchange_name,
                routing_key=self.__config.settings_for_publishing.routing_key,
                properties=properties,
                mandatory=self.__config.settings_for_publishing.mandatory,
                immediate=self.__config.settings_for_publishing.immediate,
            )
        except Exception as e:
            raise PublicationException(message, message_type) from e

        await self.__logger.debug(
            "MessageChannel: "
            "message published "
            f"message: `{message}`, "
            f"message_type: `{message_type}`. "
            f"RabbitMQ properties: `{properties}`."
        )

    @required_state(InitializedState)
    async def add_consumer(self, consumer: IConsumer) -> None:

        if self.__config.settings_for_consuming is None:
            raise MessageChannelException(
                "To consume messages, you need to specify `settings_for_consuming`."
            )

        async def consumer_wrapper(
            channel: Channel,
            body: bytes,
            envelope: Envelope,
            properties: Properties,
        ) -> None:
            nonlocal consumer

            message, message_type = self.__payload_packer.unpack_payload(body)

            try:
                await consumer(message, message_type)
            except Exception as e:
                await self.__logger.warning(
                    "MessageChannel: "
                    "message consumption error "
                    f"message: `{message}`, "
                    f"message_type: `{message_type}`.",
                    exception=e,
                )
                await channel.basic_reject(envelope.delivery_tag, requeue=True)
                return

            await channel.basic_client_ack(envelope.delivery_tag)
            await self.__logger.debug(
                "MessageChannel: "
                "message consumed "
                f"message: `{message}`, "
                f"message_type: `{message_type}`."
            )

        await self.__channel.basic_consume(
            callback=consumer_wrapper,
            queue_name=self.__config.settings_for_consuming.queue_name,
            consumer_tag=self.__config.settings_for_consuming.consumer_tag,
            no_local=self.__config.settings_for_consuming.no_local,
            no_ack=self.__config.settings_for_consuming.no_ack,
            exclusive=self.__config.settings_for_consuming.exclusive,
            no_wait=self.__config.settings_for_consuming.no_wait,
            arguments=self.__config.settings_for_consuming.arguments,
        )
