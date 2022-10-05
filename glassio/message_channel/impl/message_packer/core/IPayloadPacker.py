from typing import Optional
from typing import Tuple


__all__ = [
    "IMessagePacker",
]


class IMessagePacker:

    __slots__ = ()

    def pack_payload(self, message: bytes, message_type: Optional[str] = None) -> bytes:
        raise NotImplementedError()

    def unpack_payload(self, payload: bytes) -> Tuple[bytes, Optional[str]]:
        raise NotImplementedError()
