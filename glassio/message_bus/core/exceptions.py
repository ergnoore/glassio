from typing import Optional

from glassio.utils import GlassioException


__all__ = [
    "MessageBusException",
    "PublicationException",
    "MessageTypeMatchingException",
]


class MessageBusException(GlassioException):

    __slots__ = ()


class PublicationException(MessageBusException):

    __slots__ = ()

    def __init__(self, message: bytes, message_type: Optional[str]) -> None:
        super().__init__(
            f"Error publication a message: `{message}`, "
            f"message_type: `{message_type}`."
        )


class MessageTypeMatchingException(MessageBusException):

    __slots__ = ()

    def __init__(self, message_type: Optional[str]) -> None:
        super().__init__(
            f"Error error matching the message type and its properties "
            f"message_type: `{message_type}`."
        )
