from typing import Optional

from .RabbitMessageBusProperties import RabbitMessageBusProperties
from ....core import IMessageTypeMatcher


__all__ = [
    "DefaultMessageTypeMatcher",
]


class DefaultMessageTypeMatcher(IMessageTypeMatcher[RabbitMessageBusProperties]):

    __slots__ = ()

    def match(self, message_type: Optional[str]) -> RabbitMessageBusProperties:
        message_type = message_type or "not specified"
        return {"message_type": message_type}
