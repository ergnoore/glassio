from ..message import MessageConsumer


__all__ = [
    "IConsumptionChannel",
]


class IConsumptionChannel:

    __slots__ = ()

    async def set_consumer(self, consumer: MessageConsumer) -> None:
        raise NotImplementedError()

    async def pop_consumer(self) -> None:
        raise NotImplementedError()
