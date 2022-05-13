from typing import Optional

from .MemoryMessageBusProperties import MemoryMessageBusProperties
from ....core import IMessageTypeMatcher


__all__ = [
    "DefaultMessageTypeMatcher",
]


class DefaultMessageTypeMatcher(IMessageTypeMatcher[MemoryMessageBusProperties]):

    __slots__ = ()

    def match(self, message_type: Optional[str]) -> MemoryMessageBusProperties:
        return MemoryMessageBusProperties()
