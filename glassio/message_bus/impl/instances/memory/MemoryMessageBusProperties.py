from typing import NamedTuple
from typing import Optional


__all__ = [
    "MemoryMessageBusProperties",
]


class MemoryMessageBusProperties(NamedTuple):
    priority: Optional[int] = None
    expiration: Optional[int] = None
