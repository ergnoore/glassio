from ..message import Message


__all__ = [
    "IPublicationChannel",
]


class IPublicationChannel:

    __slots__ = ()

    async def publish(self, message: Message) -> None:
        raise NotImplementedError()
