from time import time
from typing import Optional
from typing import Tuple

from .MemoryMessageChannelProperties import MemoryMessageChannelProperties


__all__ = [
    "MessageWrapper",
]


class MessageWrapper:

    __slots__ = (
        "__message",
        "__message_type",
        "__properties",
        "__timestamp",
    )

    def __init__(
        self,
        message: bytes,
        message_type: Optional[str],
        properties: MemoryMessageChannelProperties,
    ) -> None:
        self.__message = message
        self.__message_type = message_type
        self.__properties = properties
        self.__timestamp = int(time())

    @property
    def priority(self) -> int:
        return self.__properties.priority or 0

    def unwrap(
        self,
        time_now: float,
    ) -> Tuple[bytes, Optional[str]]:

        if self.__properties.expiration is None:
            return self.__message, self.__message_type

        if self.__timestamp + \
                self.__properties.expiration >= time_now:
            return self.__message, self.__message_type

        raise TimeoutError(
            "Message ttl expired.",
            f"message: `{self.__message}`, "
            f"message_type: `{self.__message_type}`."
        )

    def __eq__(self, other: 'MessageWrapper'):
        return self.priority == other.priority

    def __lt__(self, other: 'MessageWrapper'):
        return self.priority < other.priority

    def __gt__(self, other: 'MessageWrapper'):
        return self.priority > other.priority
