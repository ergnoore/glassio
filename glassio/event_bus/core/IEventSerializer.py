from typing import Generic
from typing import Optional
from typing import Tuple
from typing import TypeVar


__all__ = [
    "IEventSerializer",
]


E = TypeVar('E')


class IEventSerializer(Generic[E]):

    __slots__ = ()

    def serialize(self, event: E) -> Tuple[bytes, Optional[str]]:
        raise NotImplementedError()

    def deserialize(
        self,
        serialized_event: bytes,
        event_type: Optional[str],
    ) -> E:
        raise NotImplementedError()
