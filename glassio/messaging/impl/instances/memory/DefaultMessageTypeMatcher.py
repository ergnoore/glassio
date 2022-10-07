from typing import Optional

from .MemoryMessageChannelProperties import MemoryMessageChannelProperties
from ....core import IMessageTypeMatcher


__all__ = [
    "DefaultMessageTypeMatcher",
]


class DefaultMessageTypeMatcher(IMessageTypeMatcher[MemoryMessageChannelProperties]):

    __slots__ = ()

    def match(self, message_type: Optional[str]) -> MemoryMessageChannelProperties:
        return MemoryMessageChannelProperties()
