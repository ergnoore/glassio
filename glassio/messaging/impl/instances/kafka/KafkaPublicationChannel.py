from .... import Message
from ....core import IPublicationChannel
from aiokafka import AIOKafkaProducer


__all__ = [
    "KafkaPublicationChannel",
]


class KafkaPublicationChannel(IPublicationChannel):

    __slots__ = ()

    async def publish(self, message: Message) -> None:
        producer = AIOKafkaProducer()
        await producer.send_and_wait("my_topic", b"Super message")