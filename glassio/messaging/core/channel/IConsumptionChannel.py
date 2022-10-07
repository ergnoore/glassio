from ..message import MessageConsumer


__all__ = [
    "IConsumptionChannel",
]


class IConsumptionChannel:

    __slots__ = ()

    async def add_consumer(self, consumer: MessageConsumer) -> None:
        raise NotImplementedError()
