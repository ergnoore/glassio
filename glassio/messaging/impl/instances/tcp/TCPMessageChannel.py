from asyncio import get_running_loop
from asyncio import open_connection
from asyncio import Task
from typing import Sequence
from asyncio import IncompleteReadError
from glassio.initializable_components import AbstractInitializableComponent
from asyncio import StreamReader
from asyncio import StreamWriter
from asyncio import create_task
from typing import Optional
from ....core import IMessageChannel
from ....core import Message
from ....core import MessageConsumer
from ...message_packer import IMessagePacker
from asyncio import CancelledError
from .TCPMessageChannelConfig import TCPMessageChannelConfig

__all__ = [
    "TCPMessageChannel",
]


class TCPMessageChannel(IMessageChannel, AbstractInitializableComponent):

    __slots__ = (
        "__config",
        "__message_packer",
        "__consumer",
        "__reader",
        "__writer",
        "__read_stream_task",
    )

    def __init__(
        self,
        config: TCPMessageChannelConfig,
        message_packer: IMessagePacker,
    ) -> None:
        super().__init__(name="TCPMessageChannel")
        self.__config = config
        self.__message_packer = message_packer
        self.__consumer: Optional[MessageConsumer] = None
        self.__reader: Optional[StreamReader] = None
        self.__writer: Optional[StreamWriter] = None
        self.__read_stream_task: Optional[Task] = None

    async def _initialize(self) -> None:
        self.__reader, self.__writer = await open_connection(
            host=self.__config.host,
            port=self.__config.port
        )
        self.__read_stream_task = create_task(self.__read_stream())

    def __split_into_chunks(self, payload: bytes, chunk_size: int) -> Sequence[bytes]:
        payload_length = len(payload)
        last_step = (payload_length // chunk_size) * chunk_size

        result = []

        for i in range(0, payload_length, chunk_size):
            chunk = payload[i: i + chunk_size]
            result.append(chunk)

        if last_step < payload_length:
            result.append(payload[last_step:])

        return result

    async def __send_bytes(self, payload: bytes) -> None:
        self.__writer.write(payload)
        await self.__writer.drain()

    async def publish(self, message: Message) -> None:
        packed_message = self.__message_packer.pack_message(message)
        chunks = self.__split_into_chunks(packed_message, self.__config.max_packet_size - 1)

        if len(chunks) == 1:
            data = b"\x01" + chunks[0]
            await self.__send_bytes(data)
            return

        for index, chunk in enumerate(chunks):
            if index == 1:
                data = b"\x00" + chunks[0]
                await self.__send_bytes(data)
                continue

            data = b"\x02" + chunk
            await self.__send_bytes(data)

    async def set_consumer(self, consumer: MessageConsumer) -> None:
        self.__consumer = consumer

    async def pop_consumer(self) -> None:
        self.__consumer = None

    async def __read_stream(self) -> None:
        try:
            message_buffer: bytearray = bytearray()
            while True:
                try:
                    packet = await self.__reader.readexactly(self.__config.max_packet_size)
                except IncompleteReadError as exc:
                    packet = exc.partial

                short_message_flag = bool.from_bytes((packet[0],), "big")

                if not short_message_flag:
                    message_buffer.append(*packet[1:])

                message = self.__message_packer.unpack_message(message_buffer)
                message_buffer.clear()

                if self.__consumer is not None:
                    await self.__consumer(message)

                message_buffer.append(*packet[1:])

        except CancelledError:
            pass

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        self.__read_stream_task.cancel()
        self.__writer.write_eof()
        await self.__writer.drain()
        self.__writer.close()
        await self.__writer.wait_closed()
