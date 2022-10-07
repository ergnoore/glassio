from glassio.utils import GlassioException

from .message import Message


__all__ = [
    "MessageChannelException",
    "ConsumptionException",
    "PublicationException",
]


class MessageChannelException(GlassioException):

    __slots__ = ()


class PublicationException(MessageChannelException):

    __slots__ = ()

    def __init__(self, message: Message) -> None:
        super().__init__(
            f"Error of publication a message: `{message}`."
        )


class ConsumptionException(MessageChannelException):

    __slots__ = ()

    def __init__(self, message: Message) -> None:
        super().__init__(
            f"Error of consumption a message: `{message}`."
        )
