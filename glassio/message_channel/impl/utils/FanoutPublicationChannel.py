from ... import Message
from ...core import IPublicationChannel


class FanoutPublicationChannel(IPublicationChannel):

    def __init__(self, channels: IPublicationChannel) -> None:
        pass

    async def publish(self, message: Message) -> None:
        pass
