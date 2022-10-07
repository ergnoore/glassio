from typing import NamedTuple
from typing import Optional


__all__ = [
    "MemoryMessageChannelProperties",
]


class MemoryMessageChannelProperties(NamedTuple):
    priority: Optional[int] = None
    expiration: Optional[int] = None
