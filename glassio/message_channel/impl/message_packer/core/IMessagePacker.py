from ....core import Message


__all__ = [
    "IMessagePacker",
]


class IMessagePacker:

    __slots__ = ()

    def pack_message(self, message: Message) -> bytes:
        raise NotImplementedError()

    def unpack_message(self, packed_message: bytes) -> Message:
        raise NotImplementedError()
